package com.mojian.service.impl;

import cn.dev33.satoken.stp.StpUtil;
import cn.hutool.core.thread.ThreadUtil;
import com.alibaba.fastjson.JSON;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.mojian.common.Constants;
import com.mojian.common.ResultCode;
import com.mojian.dto.article.ArticleQueryDto;
import com.mojian.entity.SysArticle;
import com.mojian.entity.SysCategory;
import com.mojian.entity.SysTag;
import com.mojian.exception.ServiceException;
import com.mojian.mapper.SysArticleMapper;
import com.mojian.mapper.SysCategoryMapper;
import com.mojian.mapper.SysTagMapper;
import com.mojian.service.SysArticleService;
import com.mojian.utils.AiUtil;
import com.mojian.utils.PageUtil;
import com.mojian.vo.article.ArticleListVo;
import com.mojian.vo.article.SysArticleDetailVo;
import com.vladsch.flexmark.html2md.converter.FlexmarkHtmlConverter;
import com.vladsch.flexmark.util.data.MutableDataSet;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Service
@RequiredArgsConstructor
public class SysArticleServiceImpl extends ServiceImpl<SysArticleMapper, SysArticle> implements SysArticleService {

    private final SysTagMapper sysTagMapper;

    private final AiUtil aiUtil;
    private final SysCategoryMapper sysCategoryMapper;

    @Override
    public IPage<ArticleListVo> selectPage(ArticleQueryDto articleQueryDto) {
        return baseMapper.selectPageList(PageUtil.getPage(), articleQueryDto);
    }

    @Override
    public SysArticleDetailVo detail(Integer id) {
        // 根据文章ID查询文章详细信息
        SysArticle sysArticle = baseMapper.selectById(id);

        // 创建一个新的SysArticleDetailVo对象，用于返回文章的详细信息
        SysArticleDetailVo sysArticleDetailVo = new SysArticleDetailVo();

        // 将查询到的SysArticle属性复制到SysArticleDetailVo中
        BeanUtils.copyProperties(sysArticle, sysArticleDetailVo);

        // 根据文章的分类ID查询文章所属的分类信息
        SysCategory sysCategory = sysCategoryMapper.selectById(sysArticle.getCategoryId());

        // 将查询到的分类名称设置到SysArticleDetailVo中
        sysArticleDetailVo.setCategoryName(sysCategory.getName());

        // 根据文章ID获取文章的标签列表
        List<String> tags = sysTagMapper.getTagNameByArticleId(id);

        // 将标签列表设置到SysArticleDetailVo中
        sysArticleDetailVo.setTags(tags);

        // 返回封装好的文章详细信息对象
        return sysArticleDetailVo;
    }


    @Override
    @Transactional(rollbackFor = Exception.class)
    public Boolean add(SysArticleDetailVo sysArticle) {

        SysArticle obj = new SysArticle();
        BeanUtils.copyProperties(sysArticle, obj);
        obj.setUserId(StpUtil.getLoginIdAsLong());

        //添加分类
        addCategory(sysArticle, obj);
        baseMapper.insert(obj);

        addTags(sysArticle, obj);

        ThreadUtil.execAsync(() -> {
            String prompt = obj.getContent() +
                    "。请根据以上内容，撰写一段 100 至 200 字之间的简洁介绍，适合用作网页文章摘要。（放在文章的最顶端）" +
                    "要求内容真实准确、语言简练优美，能够吸引读者继续阅读全文。" +
                    "使用 HTML 语法进行美化（如 <strong>、<em> ，在标签里加上style等），但不要使用 ~ 符号，也不要混用 Markdown 导致格式错误。" +
                    "请直接输出文章内容摘要，不要添加提示词或说明性文字。";
            String res = aiUtil.send(prompt);

            if (StringUtils.isNotBlank(res)) {
                obj.setAiDescribe(res);
                baseMapper.updateById(obj);
            }
        });
        return true;
    }




    @Override
    @Transactional(rollbackFor = Exception.class)
    public Boolean update(SysArticleDetailVo sysArticle) {

        SysArticle obj = new SysArticle();
        BeanUtils.copyProperties(sysArticle, obj);

        //没有管理员权限就只能修改自己的文章
        if (!StpUtil.hasRole(Constants.ADMIN)) {
            SysArticle article = baseMapper.selectById(sysArticle.getId());
            if (article.getUserId() != StpUtil.getLoginIdAsLong()) {
                throw new ServiceException("只能修改自己的文章");
            }
        }

        addCategory(sysArticle, obj);
        baseMapper.updateById(obj);

        //先删除标签在新增标签
        sysTagMapper.deleteArticleTagsByArticleIds(Collections.singletonList(obj.getId()));
        addTags(sysArticle, obj);
        return true;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Boolean delete(List<Long> ids) {

        //没有管理员权限就只能删除自己的文章
        if (!StpUtil.hasRole(Constants.ADMIN)) {
            List<SysArticle> sysArticles = baseMapper.selectBatchIds(ids);
            for (SysArticle sysArticle : sysArticles) {
                if (sysArticle.getUserId() != StpUtil.getLoginIdAsLong()) {
                    throw new RuntimeException("只能删除自己的文章");
                }
            }
        }

        baseMapper.deleteBatchIds(ids);
        sysTagMapper.deleteArticleTagsByArticleIds(ids);
        return true;
    }


    @Override
    public void reptile(String url) {
        try {
            Document document = Jsoup.connect(url).get();
            Elements title  = document.getElementsByClass("title-article");
            Elements tags  = document.getElementsByClass("tag-link");
            Elements content  = document.getElementsByClass("article_content");
            if (StringUtils.isBlank(content.toString())) {
                throw new ServiceException(ResultCode.CRAWLING_ARTICLE_FAILED.getDesc());
            }

            //爬取的是HTML内容，需要转成MD格式的内容
            String newContent = content.get(0).toString().replaceAll("<code>", "<code class=\"lang-java\">");
            String markdown = FlexmarkHtmlConverter.builder(new MutableDataSet()).build().convert(newContent)
                    .replace("lang-java","java");

            SysArticle entity = SysArticle.builder().userId(StpUtil.getLoginIdAsLong()).contentMd(markdown)
                    .isOriginal(Constants.NO).originalUrl(url)
                    .title(title.get(0).text()).cover("https://api.btstu.cn/sjbz/api.php?lx=dongman&format=images").content(newContent).build();

            baseMapper.insert(entity);
            //为该文章添加标签
            List<Integer> tagIds = new ArrayList<>();
            tags.forEach(item ->{
                String tag = item.text();
                SysTag result = sysTagMapper.selectOne(new LambdaQueryWrapper<SysTag>().eq(SysTag::getName,tag ));
                if (result == null){
                    result = SysTag.builder().name(tag).build();
                    sysTagMapper.insert(result);
                }
                tagIds.add(result.getId());
            });
            sysTagMapper.addArticleTagRelations(entity.getId(),tagIds);

            System.out.println("文章抓取成功，内容为:" + JSON.toJSONString(entity));
        } catch (IOException e) {
            throw new ServiceException(e.getMessage());
        }
    }

    private void addCategory(SysArticleDetailVo sysArticle, SysArticle obj) {
        SysCategory sysCategory = sysCategoryMapper.selectOne(new LambdaQueryWrapper<SysCategory>()
                .eq(SysCategory::getName, sysArticle.getCategoryName()));
        if (sysCategory == null) {
            sysCategory = SysCategory.builder().name(sysArticle.getCategoryName()).build();
            sysCategoryMapper.insert(sysCategory);
        }
        obj.setCategoryId(sysCategory.getId());
    }

    private void addTags(SysArticleDetailVo sysArticle, SysArticle obj) {
        //添加标签
        List<Integer> tagIds = new ArrayList<>();
        for (String tag : sysArticle.getTags()) {
            SysTag sysTag = sysTagMapper.selectOne(new LambdaQueryWrapper<SysTag>().eq(SysTag::getName, tag));
            if (sysTag == null) {
                sysTag = SysTag.builder().name(tag).build();
                sysTagMapper.insert(sysTag);
            }
            tagIds.add(sysTag.getId());
        }
        sysTagMapper.addArticleTagRelations(obj.getId(), tagIds);
    }
}
