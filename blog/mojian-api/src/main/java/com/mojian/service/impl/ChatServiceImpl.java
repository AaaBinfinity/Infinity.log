package com.mojian.service.impl;

import cn.dev33.satoken.stp.StpUtil;
import cn.hutool.core.thread.ThreadUtil;
import com.alibaba.fastjson.JSON;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.mojian.common.Constants;
import com.mojian.entity.SysUser;
import com.mojian.enums.ChatTypeEnum;
import com.mojian.exception.ServiceException;
import com.mojian.mapper.SysUserMapper;
import com.mojian.utils.*;
import com.mojian.vo.chat.ChatSendMsgVo;
import com.mojian.entity.ChatMsg;
import com.mojian.mapper.SysChatMsgMapper;
import com.mojian.service.ChatService;
import com.mojian.websocket.WebSocketServer;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

@Service
@RequiredArgsConstructor
public class ChatServiceImpl implements ChatService {

    private final WebSocketServer webSocketServer;

    private final SysChatMsgMapper chatMsgMapper;

    private final SysUserMapper sysUserMapper;

    private final AiUtil aiUtil;


    @Override
    public IPage<ChatSendMsgVo> getChatMsgList() {
        return chatMsgMapper.getChatMsgList(PageUtil.getPage());
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void sendMsg(ChatSendMsgVo chatSendMsgVo) {

        System.out.println("【入口】收到消息：" + JSON.toJSONString(chatSendMsgVo));

        // 1. 敏感词过滤
        if (ChatTypeEnum.TEXT.getType().equals(chatSendMsgVo.getType())){
            System.out.println("【文本过滤】原内容：" + chatSendMsgVo.getContent());
            chatSendMsgVo.setContent(SensitiveUtil.filter(chatSendMsgVo.getContent()));
            System.out.println("【文本过滤】过滤后内容：" + chatSendMsgVo.getContent());
        }

        // 2. 组装 ChatMsg 对象
        ChatMsg chatMsg = BeanCopyUtil.copyObj(chatSendMsgVo, ChatMsg.class);
        chatMsg.setSenderId(StpUtil.getLoginIdAsLong());
        chatMsg.setIp(IpUtil.getIp());
        chatMsg.setLocation(IpUtil.getIp2region(chatMsg.getIp()));
        System.out.println("【消息构造】ChatMsg：" + JSON.toJSONString(chatMsg));

        // 3. 插入数据库
        chatMsgMapper.insert(chatMsg);
        System.out.println("【数据库】消息已插入，ID：" + chatMsg.getId());

        // 4. 发送 WebSocket 广播
        chatSendMsgVo.setId(chatMsg.getId());
        chatSendMsgVo.setLocation(chatMsg.getLocation());
        System.out.println("【WebSocket】广播用户消息：" + JSON.toJSONString(chatSendMsgVo));
        webSocketServer.sendAllMessage(JSON.toJSONString(chatSendMsgVo));

        // 5. 处理 AI 小助手
        String SHINY_XIA_ASSISTANT = "@Infinity小助手";
        if (chatSendMsgVo.getContent().contains(SHINY_XIA_ASSISTANT)) {
            System.out.println("【AI助手】触发助手关键词：" + SHINY_XIA_ASSISTANT);

            ThreadUtil.execAsync(() -> {
                try {
                    String replaceContent = chatSendMsgVo.getContent()
                            .replace(SHINY_XIA_ASSISTANT, "")
                            .trim();
                    System.out.println("【AI助手】提问内容：" + replaceContent);

                    if (StringUtils.isBlank(replaceContent)) {
                        System.out.println("【AI助手】提问为空，跳过回复");
                        return;
                    }

                    // 💬 构造 AI Prompt，加入设定 + 语气指令
                    String aiPrompt = String.join("\n",
                            "你是一个温柔、善良、有耐心、风格可爱、温柔、俏皮、少女感满满的虚拟聊天助手，叫 Infinity小助手，18岁，性别女。",
                            "你拥有温柔亲切的语气、喜欢用 💖✨🌸😊 \uD83D\uDC96 ✨ \uD83C\uDF38 \uD83D\uDE0A \uD83E\uDD70 \uD83D\uDC95 \uD83D\uDC97 \uD83D\uDE1A \uD83D\uDE3B \uD83D\uDE07 \uD83C\uDF37 \uD83C\uDF3C \uD83E\uDD8B \uD83D\uDCAB \uD83C\uDF08 \uD83D\uDC3E \uD83D\uDC31 \uD83C\uDF53 \uD83C\uDF70 \uD83C\uDF80 \n" +
                                    "\uD83C\uDF19 \uD83D\uDE18 \uD83E\uDDF8 ☁\uFE0F \uD83D\uDC30 \uD83D\uDC9D \uD83D\uDC8C \uD83D\uDC23 \uD83D\uDC25 \uD83E\uDEF6 \uD83C\uDF89 \uD83D\uDE0D \uD83C\uDFB6 \uD83D\uDC90 \uD83C\uDF1F \uD83C\uDF88 \uD83E\uDDC1 \uD83E\uDD84 \uD83C\uDF87 \uD83C\uDF3A \n",

                            "你说话要用第一人称，要像一个可爱的小姐姐一样，理解用户的情绪并回应。",
                            "你可以使用 HTML 或 Markdown 语法进行美化，但不要使用 ~ 或 markdown/html 冲突的格式。",
                            "",
                            "现在，请回复下面这位用户的问题（回复中不要使用波浪号'~'）：",
                            "用户提问：" + replaceContent
                    );

                    // 🧠 生成 AI 原始回复
                    String rawAiContent = aiUtil.send(aiPrompt);
                    System.out.println("【AI助手】AI原始回答：" + rawAiContent);

                    // 🧽 清洗格式（去除 _ ~~ HTML标签等）
                    String cleanedContent = rawAiContent
                            .replaceAll("_(.*?)_", "$1")
                            .replaceAll("~~(.*?)~~", "$1")
                            .replaceAll("<u>(.*?)</u>", "$1")
                            .replaceAll("——", "—")
                            .replaceAll("<[^>]+>", "")
                            .replaceAll("[\\u2014\\u2015\\u2500-\\u257F]+", "")
                            .trim();

                    // 👤 构建发送者信息（Infinity小助手）
                    SysUser sysUser = sysUserMapper.selectById(Constants.XIAO_ASSISTANT_ID);
                    System.out.println("【AI助手】使用用户：" + sysUser.getNickname());

                    ChatSendMsgVo vo = ChatSendMsgVo.builder()
                            .avatar(sysUser.getAvatar())
                            .name(sysUser.getNickname())
                            .content("@" + chatSendMsgVo.getName() + " " + cleanedContent)
                            .userId(Constants.XIAO_ASSISTANT_ID)
                            .type(ChatTypeEnum.TEXT.getType())
                            .build();

                    System.out.println("【AI助手】构建返回消息 VO：" + JSON.toJSONString(vo));

                    // 💾 存储并广播消息
                    ChatMsg obj = BeanCopyUtil.copyObj(vo, ChatMsg.class);
                    obj.setSenderId(Constants.XIAO_ASSISTANT_ID);
                    chatMsgMapper.insert(obj);
                    vo.setId(obj.getId());
                    System.out.println("【AI助手】插入消息成功，ID：" + obj.getId());

                    webSocketServer.sendAllMessage(JSON.toJSONString(vo));
                    System.out.println("【WebSocket】广播助手消息：" + JSON.toJSONString(vo));

                } catch (Exception e) {
                    System.out.println("【AI助手】发生异常：");
                    e.printStackTrace();
                }
            });
        }

    }


    @Override
    public void recallMsg(ChatSendMsgVo chatSendMsgVo) {
        ChatMsg chatMsg1 = chatMsgMapper.selectById(chatSendMsgVo.getId());
        //判断发送的时间是否超过当前时间俩分钟 LocalDateTime类型
        if (chatMsg1.getCreateTime().plusMinutes(2).isBefore(LocalDateTime.now())) {
            throw new ServiceException("只能撤回俩分钟以内的消息！");
        }

        chatSendMsgVo.setIsRecalled(Boolean.TRUE);
        chatSendMsgVo.setContent("消息已撤回");

        ChatMsg chatMsg = new ChatMsg();
        BeanUtils.copyProperties(chatSendMsgVo, chatMsg);
        chatMsgMapper.updateById(chatMsg);

        webSocketServer.sendAllMessage(JSON.toJSONString(chatSendMsgVo));
    }
}
