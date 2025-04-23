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
        :size="drawerSize"
    >
      <!-- 视频播放 -->
      <div class="video-container">
        <video ref="video" style="width: 100%" controls :src="videoSrc" :volume="0.3"></video>
      </div>
      <div style="margin-left: 20px; margin-top: 10px">
        <el-button type="primary" :icon="btnIcon" size="small" @click="operateVideo">
          {{ btnContent }}
        </el-button>
        <el-button type="primary" icon="el-icon-arrow-right" size="small" @click="nextVideo">下一个视频</el-button>
      </div>

      <!-- 音乐角模块 -->
      <div class="music-player" v-if="music.url">
        <div class="music-header">
          <div class="music-title">
            <h5>🎵 音乐角</h5>
            <p class="music-name" :title="music.name">{{ music.name }}</p>
          </div>
          <button @click="fetchMusic" class="music-refresh-btn">换一首</button>
        </div>
        <audio :src="music.url" controls class="music-audio" :volume="0.3"></audio>
      </div>
    </el-drawer>
  </div>
</template>




<script>
import axios from 'axios'

export default {
  name: 'RandomVideo',
  data() {
    return {
      drawer: false,
      videoSrc: 'http://api.yujn.cn/api/zzxjj.php',
      isPlaying: true,
      btnContent: '暂停',
      btnIcon: 'el-icon-video-pause',
      drawerSize: '30%',
      music: {
        name: '',
        url: ''
      }
    }
  },
  mounted() {
    this.fetchMusic();  // 确保组件加载时就开始获取音乐数据
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
    nextVideo() {
      this.videoSrc = 'http://api.yujn.cn/api/zzxjj.php?temps=' + new Date().getTime();
    },
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
    },
    fetchMusic() {
      axios.get('http://127.0.0.1:5000/api/music').then(res => {
        this.music = res.data.music || {};
      }).catch(() => {
        this.$message.error('获取音乐失败');
      });
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

.music-player {
  margin: 12px 20px 0;
  padding: 8px 12px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(142, 142, 142, 0.73);
  backdrop-filter: blur(4px);
}

.music-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.music-title {
  display: flex;
  flex-direction: column;
}

.music-title h5 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: $primary;
  line-height: 1.2;
}

.music-name {
  font-size: 12px;
  color: $primary;
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
}

.music-refresh-btn {
  background-color: transparent;
  color: #409eff;
  border: 1px solid #409eff;
  padding: 4px 10px;
  font-size: 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s;
}

.music-refresh-btn:hover {
  background-color: #409eff;
  color: white;
}

.music-audio {
  width: 100%;
  height: 28px;
  border-radius: 6px;
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


