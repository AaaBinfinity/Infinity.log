<template>
  <div class="contribution-graph-container">
    <!-- ECharts 热力图 -->
    <div class="echarts-container">
      <div id="echarts-heatmap" style="width:1350px; height: 280px;"></div>
    </div>
  </div>
</template>

<style scoped>
.echarts-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  height: 100%;            /* 确保父容器的高度充满可用空间 */
}


</style>



<script setup lang="ts">
import { onMounted, computed, ref, watch, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts/core';
import { CalendarComponent, VisualMapComponent } from 'echarts/components';
import { HeatmapChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';

// ECharts setup
echarts.use([CalendarComponent, VisualMapComponent, HeatmapChart, CanvasRenderer]);
dayjs.locale('zh-cn');

const props = defineProps<{
  data: Array<{
    date: string;
    count: number;
  }>;
}>();
const heatmapChart = ref<echarts.ECharts | null>(null);
const currentYear = dayjs().year();
const startDate = dayjs(`${currentYear}-01-01`);
const endDate = dayjs(`${currentYear}-12-31`);

const formattedData = computed(() =>
    props.data?.map(item => ({
      date: dayjs(item.date, 'YYYY年M月D日').format('YYYY-MM-DD'),
      count: item.count
    })) || []
);

const mergedData = computed(() => {
  const dataMap = new Map(formattedData.value.map(item => [item.date, item.count]));
  const result = [];
  let currentDate = startDate;

  while (currentDate.isBefore(endDate) || currentDate.isSame(endDate, 'day')) {
    const dateStr = currentDate.format('YYYY-MM-DD');
    result.push({
      date: dateStr,
      count: dataMap.get(dateStr) ?? 0
    });
    currentDate = currentDate.add(1, 'day');
  }

  return result;
});
const initHeatmap = () => {
  const chartDom = document.getElementById('echarts-heatmap');
  if (!chartDom) return;

  heatmapChart.value = echarts.init(chartDom);
  updateHeatmap();
};
const updateHeatmap = () => {
  if (!heatmapChart.value) return;
  const maxCount = Math.max(...mergedData.value.map(item => item.count), 1);
  const heatmapData = mergedData.value.map(item => [item.date, item.count]);
  const option = {
    tooltip: {
      position: 'top',
      formatter: (params: any) =>
          `${dayjs(params.data[0]).format('YYYY年M月D日')} · ${params.data[1]} 次贡献`
    },
    visualMap: {
      min: 0,
      max: maxCount,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 10,
      inRange: {
        color: ['rgba(234,238,246,0.62)', 'rgba(179,207,255,0.62)', 'rgba(102,153,255,0.62)', 'rgba(51,102,255,0.62)', '#0033cc']
      }
    },
    calendar: {
      range: currentYear,
      cellSize: [24, 24],  // 格子尺寸
      top: 30,
      left: 30,
      right: 30,
      bottom: 80,
      itemStyle: {
        borderWidth: 1,
        borderRadius: 6,  // 设置圆角
        borderColor: '#b8b5b5',  // 边框颜色
      },
      yearLabel: { show: false }
    },


    series: {
      type: 'heatmap',
      coordinateSystem: 'calendar',
      data: heatmapData,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  };

  heatmapChart.value.setOption(option);
};


const handleResize = () => heatmapChart.value?.resize();

onMounted(() => {
  initHeatmap();
  window.addEventListener('resize', handleResize);
});
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  heatmapChart.value?.dispose();
});

watch(mergedData, updateHeatmap);
</script>
