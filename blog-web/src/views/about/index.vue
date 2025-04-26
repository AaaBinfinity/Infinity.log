<template>

  <div class="about-page">

    <div class="about-card">


      <!-- 个人介绍部分 -->
      <div class="intro-section">
        <img src="https://foruda.gitee.com/avatar/1725543121594546085/14873817_binfinity_1725543121.png" alt="我的头像"
             class="avatar"/>
        <div class="intro-text">
          <h1>About Binfinity</h1>


          <p>// 如果人生是一个while循环的话........ <br>// 那目前这行代码就是 “continue;”</p>
          <p><br>
            姓名：Binfinity<br>
            性别：男 <br>
            年龄：<span id="age"></span><br>
            所在地：China
          </p>
        </div>
      </div>


      <div>
        <div class="quote-container">
          <p>🕒 当前时间：{{ currentTime }}
            ~~~🎲 今天你是一个：<strong>{{ programmerTitle }}</strong></p>
          <p class="quote-text">{{ currentQuote }}
            <button class="change-quote-button" @click="changeQuote">换一句</button>
          </p>
          <p>🌌 Infinity.log，是我在漫漫星河中留下一道道微光的方式。 生命的轨迹，也许无法预测，但我希望，它至少能被记录。</p>
          <p>希望多年以后再回望，看到了不止是沙发上的屁股印，还有这个博客，静静地说着： “你曾热烈地活过。”</p>
        </div>
      </div>

      <!-- 技能栈部分 -->
      <section>
        <h2>🛠 技能栈</h2>

        <div>
          <p><strong>前端：</strong> Vue 3 / TypeScript / HTML5 / CSS3</p>
          <div class="progress-bar">
            <div class="progress" style="width: 90%;"></div>
          </div>
        </div>
        <br>
        <div>
          <p><strong>后端：</strong> Flask / Spring Boot / Spring Cloud</p>
          <div class="progress-bar">
            <div class="progress" style="width: 80%;"></div>
          </div>
        </div>
        <br>
        <div>
          <p><strong>数据分析与可视化：</strong> Python / MySQL / Echarts </p>
          <div class="progress-bar">
            <div class="progress" style="width: 85%;"></div>
          </div>
        </div>
        <br>
        <div>
          <p><strong>工具与环境：</strong> Git / Linux / VSCode / 数据可视化设计</p>
          <div class="progress-bar">
            <div class="progress" style="width: 75%;"></div>
          </div>
        </div>
        <div class="tech-journey">
          <h2 class="title">🧠 我的技术成长轨迹</h2>
          <p>
            第一次接触代码，是在高考刚结束的那个暑假。最开始接触的是 Python，第一个写的程序，是用来判断一个整数是奇数还是偶数。
            那时候对“编程”这回事几乎一无所知，只是觉得：<strong>屏幕上能运行起来，真的很神奇。</strong>
          </p>
          <p>
            真正开始系统学习编程，是大一刚入学的时候。从零开始自学前端，记得那会儿写的第一个程序是 HTML 个人简历，整整调了三天三夜，
            最后才发现，出问题的地方只是一行超链接的路径写错了。虽然抓耳挠腮、焦头烂额，但也正是在这样的时刻，我第一次体会到写代码的“痛并快乐着”。
          </p>
          <p>
            后来慢慢开始做项目，走进了 Python、算法、数据分析、可视化这片浩瀚的海洋。一路上时而兴奋，时而失落，
            时常质疑自己的能力，也曾动摇过是否该继续。但每次想放弃的时候，我都会打开 VSCode，看看自己曾写过的代码，
            那一行行熟悉的字符，就像是一种力量，让我安心，也让我坚持了下来。
          </p>
        </div>
      </section>

      <!-- 项目经历部分 -->
      <section>
        <h2>📂 项目经历</h2>
        <ul>
          <li>
            <strong>社交网络图谱系统：</strong> 基于聊天频率构建用户图谱，使用 PageRank 算法计算影响力；前后端分离，Flask
            提供接口，Vue + Echarts 实现可视化交互。
          </li>
          <li>
            <strong>空气质量预警平台：</strong> 基于 LSTM 深度学习模型进行空气质量预测，当甲醛浓度异常自动触发预警，并通过图表展示变化趋势。
          </li>
          <li>
            <strong>医院预约管理系统：</strong> 实现挂号、医生查看、管理员管理等完整流程，使用 Spring Boot + Vue 实现分角色功能模块。
          </li>
        </ul>
      </section>

      <section>
        <h2>🧠 技术知识小测验</h2>
        <p><strong>{{ currentQuiz.question }}</strong></p>
        <ul>
          <li v-for="option in currentQuiz.options" :key="option">
            <label>
              <input type="radio" v-model="userAnswer" :value="option"/>
              {{ option }}
            </label>
          </li>
        </ul>
        <button @click="submitQuiz">提交答案</button>
        <button @click="nextQuiz" style="margin-left: 10px;">下一题</button>
        <p>{{ feedback }}</p>
      </section>


      <section>
        <h2>📷 Pictures</h2>
        <div class="photo-gallery">
          <img v-for="img in galleryImages" :src="img.src" :alt="img.alt" @click="openPreview(img.src)"
               class="photo-thumb"/>
        </div>

        <div v-if="showPreview" class="preview-mask" @click="closePreview">
          <img :src="previewImage" class="preview-img"/>
        </div>
      </section>

    </div>
  </div>
</template>

<script>
export default {
  name: 'About',
  data() {
    return {
      showBackTop: false,
      currentTime: '',
      programmerTitle: '',
      quizData: [],
      currentQuiz: {
        question: "",
        options: [],
        answer: ""
      },
      userAnswer: '',
      feedback: '',
      quotes: [],
      currentQuote: "",
      galleryImages: [],
      titles: [],
      showPreview: false,
      previewImage: '',
    };
  },
  mounted() {
    this.fetchAllData();
    this.updateTime();
    setInterval(this.updateTime, 1000);

    const birthYear = 2005;
    const currentYear = new Date().getFullYear();
    const age = currentYear - birthYear;
    document.getElementById('age').textContent = age;

    window.addEventListener('scroll', this.checkScroll);
  },

  beforeDestroy() {
    window.removeEventListener('scroll', this.checkScroll);
  },

  methods: {
    async fetchAllData() {
      await Promise.all([
        this.fetchQuizData(),
        this.fetchQuotes(),
        this.fetchGalleryImages(),
        this.fetchProgrammerTitles()
      ]);

      this.loadQuiz();
      this.changeQuote();
      this.generateProgrammerTitle();
    },

    async fetchQuizData() {
      try {
        const res = await fetch('https://infinitylog.top/api1314/api/quiz');
        const data = await res.json();
        this.quizData = data.data || [];
      } catch (e) {
      }
    },

    async fetchQuotes() {
      try {
        const res = await fetch('https://infinitylog.top/api1314/api/quotes');
        const data = await res.json();
        this.quotes = data.data || [];
      } catch (e) {
      }
    },

    async fetchGalleryImages() {
      try {
        const res = await fetch('https://infinitylog.top/api1314/api/images');
        const data = await res.json();
        this.galleryImages = data.images || [];
      } catch (e) {
      }
    },

    async fetchProgrammerTitles() {
      try {
        const res = await fetch('https://infinitylog.top/api1314/api/titles');
        const data = await res.json();
        this.titles = data.data || [];
      } catch (e) {
      }
    },

    loadQuiz() {
      const index = Math.floor(Math.random() * this.quizData.length);
      this.currentQuiz = this.quizData[index] || {question: '', options: [], answer: ''};
      this.userAnswer = '';
      this.feedback = '';
    },

    submitQuiz() {
      if (!this.userAnswer) {
        this.feedback = "⚠️ 请先选择一个选项！";
        return;
      }
      if (this.userAnswer === this.currentQuiz.answer) {
        this.feedback = "🎉 回答正确！你太棒了~";
      } else {
        this.feedback = `❌ 答错啦！正确答案是：${this.currentQuiz.answer}`;
      }
    },

    nextQuiz() {
      this.loadQuiz();
    },

    checkScroll() {
      this.showBackTop = window.scrollY > 100;
    },

    scrollToTop() {
      window.scrollTo({top: 0, behavior: 'smooth'});
    },

    updateTime() {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString();
    },

    changeQuote() {
      const randomIndex = Math.floor(Math.random() * this.quotes.length);
      this.currentQuote = this.quotes[randomIndex] || "";
    },

    generateProgrammerTitle() {
      const index = Math.floor(Math.random() * this.titles.length);
      this.programmerTitle = this.titles[index] || "";
    },

    openPreview(imgUrl) {
      this.previewImage = imgUrl;
      this.showPreview = true;
    },

    closePreview() {
      this.showPreview = false;
    },
  }
};
</script>

<style lang="scss" scoped>
$primary-color: #007acc;
$success-color: #4caf50;
$text-color: rgb(57, 57, 57);
$subtitle-color: #515151;
$bg-light: rgba(251, 251, 251, 0);

.about-page {
  display: flex;
  justify-content: center;
  padding: 2rem;
  background-color: $bg-light;
}

.about-card {
  max-width: 1000px;
  width: 100%;
  padding: 2rem;
  border-radius: 16px;
  background: rgba(218, 218, 218, 0.19);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  color: $text-color;
  line-height: 1.8;

  section {
    margin-top: 2rem;
  }

  h1 {
    margin-bottom: 0.5rem;
    font-size: 2rem;
    font-weight: 600;
  }

  h2 {
    position: relative;
    font-size: 1.5rem;
    color: $primary-color;
    margin-top: 1.5rem;

    &::after {
      content: '';
      display: block;
      width: 60px;
      height: 4px;
      background-color: $primary-color;
      margin-top: 0.5rem;
      border-radius: 2px;
    }
  }

  ul {
    padding-left: 1.5em;

    li {
      margin-bottom: 0.5em;
      list-style-type: disc;
    }
  }

  .intro-section {
    display: flex;
    align-items: center;
    margin-bottom: 2rem;

    .avatar {
      width: 240px;
      height: 240px;
      border-radius: 50%;
      object-fit: cover;
      margin-right: 2rem;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.82);
    }

    .intro-text {
      flex: 1;

      .subtitle {
        font-size: 1.1rem;
        color: $subtitle-color;
        margin: 0.5rem 0 1rem;
      }
    }
  }

  .photo-gallery {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;

    .photo-thumb {
      width: 300px;
      object-fit: cover;
      border-radius: 8px;
      cursor: pointer;
      transition: transform 0.3s ease;

      &:hover {
        transform: scale(1.05);
      }
    }
  }

  .section-image {
    width: 100%;
    margin-top: 1rem;
    border-radius: 8px;
  }

  .preview-mask {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 999;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;

    .preview-img {
      max-width: 90%;
      max-height: 80%;
      border-radius: 10px;
    }
  }

  .progress-bar {
    background-color: rgba(255, 255, 255, 0.42);
    border-radius: 8px;
    height: 8px;
    margin: 5px 0;

    .progress {
      background-color: $success-color;
      height: 100%;
      border-radius: 8px;
    }
  }

  .back-to-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background-color: $primary-color;
    color: rgba(255, 255, 255, 0);
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s;

    &:hover {
      background-color: darken($primary-color, 10%);
    }
  }
}

.quote-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;

  .quote-text {
    font-size: 1.5rem;
    margin-bottom: 20px;
    color: $text-color;
    text-align: center;
  }

  .change-quote-button {
    background-color: $success-color;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    padding: 8px 16px;
    font-size: 1rem;
    transition: background-color 0.3s;

    &:hover {
      background-color: darken($success-color, 10%);
    }
  }
}

@media (max-width: 768px) {
  .about-page {
    padding: 1rem;
  }

  .about-card {
    padding: 1rem;
    border-radius: 12px;

    h1 {
      font-size: 1.5rem;
    }

    h2 {
      font-size: 1.2rem;
    }

    .intro-section {
      flex-direction: column;
      text-align: center;

      .avatar {
        width: 160px;
        height: 160px;
        margin-bottom: 1rem;
      }

      .intro-text {
        .subtitle {
          font-size: 1rem;
          margin: 0.5rem 0;
        }
      }
    }

    .photo-gallery {
      gap: 8px;

      .photo-thumb {
        width: 100%;
      }
    }

    .section-image {
      border-radius: 6px;
      margin-top: 0.5rem;
    }

    ul li {
      margin-bottom: 0.4em;
    }

    .back-to-top {
      bottom: 1rem;
      right: 1rem;
      width: 36px;
      height: 36px;
      font-size: 1.2rem;
    }
  }

  .quote-container {
    margin-top: 20px;

    .quote-text {
      font-size: 1.2rem;
      margin-bottom: 12px;
    }

    .change-quote-button {
      font-size: 0.9rem;
      padding: 6px 12px;
    }
  }
}
</style>
