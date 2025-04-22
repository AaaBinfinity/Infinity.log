<template>
    <div class="random-video">
        <div class="random-video-btn">
            <el-tooltip class="box-item" effect="dark" content="通往神秘世界" placement="right">
                <div @click="drawer = true">
                    <i class="el-icon-d-arrow-right"></i>
                </div>
            </el-tooltip>
        </div>

      <el-drawer
          title="随机视频播放"
          :visible.sync="drawer"
          :with-header="false"
          :size="drawerSize">

      <div class="video-container">
                <video ref="video" style="width: 100%" controls autoplay :src="videoSrc"></video>
            </div>
            <div style="margin-left: 20px; margin-top: 10px">
                <el-button type="primary" :icon="btnIcon" size="small" @click="operateVideo">
                    {{ btnContent }}
                </el-button>
                <el-button type="primary" icon="el-icon-arrow-right" size="small" @click="nextVideo">下一个视屏</el-button>
            </div>
        </el-drawer>
    </div>
</template>

<script>
export default {
  name: 'RandomVideo',
  data() {
    return {
      drawer: false,
      videoSrc: 'http://api.yujn.cn/api/zzxjj.php',
      isPlaying: true,
      btnContent: '暂停',
      btnIcon: 'el-icon-video-pause',
      drawerSize: '30%' // 默认宽度
    }
  },
  mounted() {
    this.setDrawerSize();
    window.addEventListener('resize', this.setDrawerSize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.setDrawerSize);
  },
  methods: {
    setDrawerSize() {
      this.drawerSize = window.innerWidth < 768 ? '90%' : '30%';
    },
    // 切换视频
    nextVideo() {
      this.videoSrc = 'http://api.yujn.cn/api/zzxjj.php?temps=' + new Date().getTime();
    },
    // 暂停和开启视频
    operateVideo() {
      if (this.isPlaying) {
        this.$refs.video.pause();
        this.btnContent = '播放';
        this.btnIcon = 'el-icon-video-play';
        this.isPlaying = false;
      } else {
        this.$refs.video.play();
        this.btnContent = '暂停';
        this.btnIcon = 'el-icon-video-pause';
        this.isPlaying = true;
      }
    }
  }
}

</script>

<style scoped lang="scss">
.random-video-btn {
    position: fixed;
    left: 10px;
    bottom: 10%;
    font-size: 1.5rem;
    color: $primary;
    cursor: pointer;
}

.video-container {
    padding: $spacing-sm;
    border-radius: $border-radius-md;
    video {
        border-radius: $border-radius-md;
    }
}

@media (max-width: 768px) {
  .random-video-btn {
    font-size: 1.2rem;
    left: 5px;
    bottom: 8%;
  }

  .video-container {
    padding: 10px;

    video {
      width: 100%;
      height: auto;
    }
  }

  .el-drawer {
    width: 100% !important;
  }
}

</style>
