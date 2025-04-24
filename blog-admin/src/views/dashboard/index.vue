<template>
  <div class="dashboard-container">
    <!-- 数据卡片 -->
    <el-row :gutter="20">
      <el-col :span="6" v-for="(item, index) in statistics" :key="item.title">
        <el-card
          shadow="hover"
          :body-style="{ padding: '20px' }"
          class="data-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="card-content">
            <div class="icon-wrapper" :class="item.type">
              <el-icon><component :is="item.icon" /></el-icon>
            </div>
            <div class="data-wrapper">
              <count-to
                :start-val="0"
                :end-val="item.value"
                :duration="2000"
                class="card-value"
              />
              <div class="card-title">{{ item.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>


    <el-row :gutter="20" class="chart-row">
      <el-col :span="24">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <span>文章贡献图</span>
          </template>
          <ContributionGraph :data="contributionData" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="6">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>词云图</span>
            </div>
          </template>
          <div ref="wordCloudRef" class="chart"></div>
        </el-card>
      </el-col>


      <el-col :span="8">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>分类统计</span>
            </div>
          </template>
          <div ref="pieChartRef" class="chart"></div>
        </el-card>
      </el-col>

      <el-col :span="10">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>贡献趋势</span>
            </div>
          </template>
          <div ref="contributeRef" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>

  </div>
</template>

<script setup lang="ts">

import type { EChartsOption } from 'echarts'
import {
  CaretTop,
  CaretBottom,
  Document,
  Collection,
  ChatLineRound,
  View
} from '@element-plus/icons-vue'
import CountTo from '@/views/dashboard/components/CountTo.vue'
import ContributionGraph from './components/ContributionGraph.vue'
import { getDashboardDataApi, getBottomDataApi } from '@/api/system'

import 'echarts-wordcloud'
import * as echarts from 'echarts'
import { ref, onMounted } from 'vue'




// 贡献趋势图相关
const contributeRef = ref<HTMLElement>()

// 获取趋势图数据
const getContributionData = async () => {
  try {
    const res = await fetch('http://infinitylog.top:1314/api/contributions')
    const data = await res.json()

    // 处理日期格式和填充数据
    const today = new Date()
    const result = []

    // 生成最近30天的日期映射表
    const dateMap = new Map()
    data.contributions.forEach((item: { day: string, count: number }) => {
      dateMap.set(item.day, item.count)
    })

    // 填充完整30天数据
    for (let i = 29; i >= 0; i--) {
      const date = new Date(today)
      date.setDate(date.getDate() - i)
      const dateString = date.toISOString().split('T')[0]
      const formattedDate = `${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`

      result.push({
        day: formattedDate,
        count: dateMap.get(formattedDate) || 0 // 使用格式化后的日期
      })
    }

    return result
  } catch (error) {
    console.error('获取贡献数据失败', error)
    return []
  }
}

// 获取趋势图配置
const getContributionOption = (contributionData: any[]): EChartsOption => {
  // 计算后30%数据的起始位置
  const startIndex = Math.floor(contributionData.length * 0.7)

  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const data = params[0]
        return `日期：${data.name}<br/>数量：${data.value}`
      }
    },
    xAxis: {
      type: 'category',
      data: contributionData.map(item => item.day),
      axisLabel: {
        interval: 0,
        rotate: 45 // 日期标签旋转45度防止重叠
      }
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: contributionData.map(item => item.count),
      type: 'line',
      smooth: true,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(64,158,255,0.8)' },
          { offset: 1, color: 'rgba(64,158,255,0.1)' }
        ])
      },
      lineStyle: {
        width: 3,
        color: '#409EFF'
      },
      itemStyle: {
        color: '#409EFF'
      },
      markPoint: {
        data: [
          { type: 'max', name: '峰值' },
          { type: 'min', name: '谷值' }
        ],
        symbolSize: 50,
        label: {
          color: '#fff',
          fontSize: 14
        }
      },
      animationDuration: 2000,
      animationEasing: 'cubicOut'
    }],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%', // 增加底部间距适应旋转标签
      containLabel: true
    },
    dataZoom: [
      {
        type: 'slider',
        show: true,
        start: (startIndex / contributionData.length) * 100,  // 设置起始位置为后30%
        end: 100, // 默认显示最后30%的数据
        handleSize: '8%',
        handleStyle: {
          backgroundColor: '#409EFF',
        },
        textStyle: {
          color: '#666'
        }
      }
    ]
  }
}

// 初始化趋势图（保持相同）
const initContributionChart = async () => {
  const contributionData = await getContributionData()
  if (contributeRef.value) {
    const contributionChart = echarts.init(contributeRef.value)
    contributionChart.setOption(getContributionOption(contributionData))
    window.addEventListener('resize', () => contributionChart.resize())
  }
}

onMounted(() => {
  initContributionChart()
})





// 词云图相关
const wordCloudRef = ref<HTMLElement>()

// 获取词云图数据
const getWordCloudData = async () => {
  try {
    const res = await fetch('http://infinitylog.top:1314/api/keywords')
    const data = await res.json()

    // 假设返回的数据格式为 { keywords: [{ keyword: 'Vue', frequency: 100, color: '#00FF00' }, ...] }
    return data.keywords.map((item: { keyword: string, frequency: number, color: string }) => ({
      name: item.keyword,
      value: item.frequency,
      color: item.color // 添加颜色字段
    }))
  } catch (error) {
    console.error('获取词云数据失败', error)
    return []
  }
}

// 更新词云图配置函数
const getWordCloudOption = (wordData: any[]): EChartsOption => ({
  tooltip: { show: true, formatter: '{b}: {c}' },
  series: [{
    type: 'wordCloud',
    shape: 'circle',
    sizeRange: [15, 50],
    rotationRange: [-60, 60],
    rotationStep: 25,
    gridSize: 8,
    drawOutOfBound: false,
    // 使用textStyle.color来设置颜色
    textStyle: {
      color: (params) => params.data.color // 直接从数据中获取颜色
    },
    data: wordData.map((item) => ({
      name: item.name,
      value: item.value,
      color: item.color // 保留颜色字段供textStyle使用
    })),
    emphasis: {
      focus: 'self', // 添加聚焦效果
      textStyle: {
        shadowBlur: 10,
        shadowColor: '#333'
      }
    },
    animationDuration: 1000,
    animationEasing: 'elasticOut',
    animationDurationUpdate: 3000,
    animationEasingUpdate: 'elasticOut'
  }]
});

// 初始化词云图时确保数据正确传递
const initWordCloudChart = async () => {
  const wordData = await getWordCloudData();
  if (wordCloudRef.value) {
    const wordCloudChart = echarts.init(wordCloudRef.value);
    wordCloudChart.setOption(getWordCloudOption(wordData));
    // 强制重绘以触发动画
    setTimeout(() => wordCloudChart.resize(), 0);
  }
};
onMounted(() => {
  initWordCloudChart()
});


const icons = {
  Document: markRaw(Document),
  Collection: markRaw(Collection),
  ChatLineRound: markRaw(ChatLineRound),
  View: markRaw(View),
  CaretTop: markRaw(CaretTop),
  CaretBottom: markRaw(CaretBottom)
}

const statistics = ref([
  {
    title: '文章总数',
    value: 0,
    type: 'primary',
    icon: icons.Document
  },
  {
    title: '用户总数',
    value: 0,
    type: 'success',
    icon: icons.Collection
  },
  {
    title: '留言总数',
    value: 0,
    type: 'warning',
    icon: icons.ChatLineRound
  },
  {
    title: '访问量',
    value: 0,
    type: 'info',
    icon: icons.View
  }
])

const contributionData = ref([])
const pieChartRef = ref<HTMLElement>()
const lineChart = shallowRef<echarts.ECharts | null>(null)
const pieChart = shallowRef<echarts.ECharts | null>(null)


// 饼图配置
const getPieChartOption = (): EChartsOption => ({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [{
    name: '分类统计',
    type: 'pie',
    radius: ['40%', '70%'],
    avoidLabelOverlap: false,
    itemStyle: {
      borderRadius: 10,
      borderColor: '#fff',
      borderWidth: 2
    },
    label: {
      show: false,
      position: 'center'
    },
    emphasis: {
      label: {
        show: true,
        fontSize: 20,
        fontWeight: 'bold'
      }
    },
    labelLine: {
      show: false
    },
    data: [] as any[]
  }]
})

// 初始化图表
const initCharts = () => {
  getBottomDataApi().then(res => {


    if (pieChartRef.value) {
      pieChart.value = echarts.init(pieChartRef.value)
        const option = getPieChartOption()
        if (option.series && Array.isArray(option.series)) {
          option.series[0].data = res.data
        }
        pieChart.value?.setOption(option)
    }
  })

}

// 处理窗口大小变化
const handleResize = () => {
  lineChart.value?.resize()
  pieChart.value?.resize()
}


onMounted(() => {
  getDashboardDataApi().then(res => {
    statistics.value[0].value = res.data.articleCount
    statistics.value[1].value = res.data.userCount
    statistics.value[2].value = res.data.messageCount
    statistics.value[3].value = res.data.visitCount
    contributionData.value = res.data.contributionData
    initCharts()
  })
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  lineChart.value?.dispose()
  pieChart.value?.dispose()
})
</script>

<style scoped>

/* 数据卡片样式 */
.data-card {
  animation: slideUp 0.5s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s;
}

.icon-wrapper:hover {
  transform: scale(1.1);
}

.icon-wrapper .el-icon {
  font-size: 30px;
  color: #fff;
}

.icon-wrapper.primary {
  background: linear-gradient(135deg, #1890ff, #36a9ff);
}

.icon-wrapper.success {
  background: linear-gradient(135deg, #52c41a, #73d13d);
}

.icon-wrapper.warning {
  background: linear-gradient(135deg, #faad14, #ffc53d);
}

.icon-wrapper.info {
  background: linear-gradient(135deg, #13c2c2, #36cfc9);
}

.data-wrapper {
  flex: 1;
}

.card-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
  margin-bottom: 8px;
}

.card-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 12px;
}

/* 图表区域样式 */
.chart-row {
  margin-top: 20px;
}

.chart {
  height: 450px;
  width: 100%;
}

.chart-card {
  height: auto;
  margin-bottom: 20px;
}

/* 暗色主题适配 */
@media (prefers-color-scheme: dark) {
  .card-value {
    color: #e6e6e6;
  }

  .chart-placeholder {
    background: #1a1a1a;
    color: #909399;
  }
}
</style>