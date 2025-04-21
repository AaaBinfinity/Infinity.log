<template>

  <div class="about-page">

    <div class="about-card">


      <!-- 个人介绍部分 -->
      <div class="intro-section">
        <img src="https://foruda.gitee.com/avatar/1725543121594546085/14873817_binfinity_1725543121.png" alt="我的头像" class="avatar" />
        <div class="intro-text">
          <h1>About Binfinity</h1>


          <p class="subtitle">// 如果人生是一个while循环的话........ <br>// 那目前这行代码就是 “continue;”</p>
          <p>
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
            <button class="change-quote-button" @click="changeQuote">换一句</button></p>
<p>🌌 Infinity.log，是我在漫漫星河中留下一道道微光的方式。 生命的轨迹，也许无法预测，但我希望，它至少能被记录。</p>
<p>希望多年以后再回望，看到了不止是沙发上的屁股印，还有这个博客，静静地说着： “你曾热烈地活过。”</p>
        </div>
      </div>
      <!-- 返回顶部按钮 -->
      <button v-if="showBackTop" class="back-to-top" @click="scrollToTop">↑</button>

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
          <p><strong>后端：</strong> Flask / Spring Boot /  Spring Cloud</p>
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
            <strong>社交网络图谱系统：</strong> 基于聊天频率构建用户图谱，使用 PageRank 算法计算影响力；前后端分离，Flask 提供接口，Vue + Echarts 实现可视化交互。
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
              <input type="radio" v-model="userAnswer" :value="option" />
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
          <img v-for="img in galleryImages" :src="img.src" :alt="img.alt" @click="openPreview(img.src)" class="photo-thumb" />
        </div>

        <div v-if="showPreview" class="preview-mask" @click="closePreview">
          <img :src="previewImage" class="preview-img" />
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
      quizData: [
        {
          "question": "猫为什么总是能跳得很高？",
          "options": ["它们有弹簧骨头", "后腿肌肉发达", "它们是魔法动物", "骨头比人少"],
          "answer": "后腿肌肉发达"
        },
        {
          "question": "洗手时用冷水和热水哪种更能去除细菌？",
          "options": ["热水", "冷水", "只用水温没关系", "必须是冰水"],
          "answer": "只用水温没关系"
        },
        {
          "question": "香蕉为什么能让人心情变好？",
          "options": ["因为它是黄色的", "富含钾", "含有让人快乐的物质", "糖分高"],
          "answer": "含有让人快乐的物质"
        },
        {
          "question": "鸡蛋壳上常见的红色印章表示什么？",
          "options": ["鸡的品种", "鸡的生日", "鸡蛋的新鲜程度", "来源追溯编码"],
          "answer": "来源追溯编码"
        },
        {
          "question": "为什么喝咖啡会让人更精神？",
          "options": ["它是黑色的", "含有咖啡因", "喝的时候在清醒", "因为它苦"],
          "answer": "含有咖啡因"
        },
        {
          "question": "为什么冰淇淋吃太快会头痛？",
          "options": ["太冷引起脑血管收缩", "甜食刺激神经", "吃得太快吓到大脑", "大脑以为你要被冻死"],
          "answer": "太冷引起脑血管收缩"
        },
        {
          "question": "人的哪个器官没有血液供应？",
          "options": ["舌头", "角膜", "耳朵", "鼻子"],
          "answer": "角膜"
        },
        {
          "question": "为什么洋葱会让人流泪？",
          "options": ["它在报复人类", "含有刺激性气体", "太辣了", "因为情绪共鸣"],
          "answer": "含有刺激性气体"
        },
        {
          "question": "蜂蜜不会变质的原因是？",
          "options": ["它是天然防腐剂", "糖分高，细菌难生存", "蜂蜜有魔法", "因为是密封的"],
          "answer": "糖分高，细菌难生存"
        },
        {
          "question": "笑一笑真的有助于身体健康吗？",
          "options": ["是的，会释放多巴胺", "不会，只是开心", "没有科学依据", "笑多了容易累"],
          "answer": "是的，会释放多巴胺"
        }
      ]
      ,
      currentQuiz: {
        question: "",
        options: [],
        answer: ""
      },
      userAnswer: '',
      feedback: '',
      quizIndex: 0,
      galleryImages: [
        { src: "http://susgtyiom.hb-bkt.clouddn.com/20250418/article-cover/36_0a2b8b0da3abaed1e81634ea9ed8af40.jpg"},
        { src: "http://susgtyiom.hb-bkt.clouddn.com/20250418/moment/65_87faa7dec45f35173ebec031edcb48ef.jpg"},
        { src: "http://susgtyiom.hb-bkt.clouddn.com/20250421/photo/24_6950c1dae63f7acba4fa1f6fd48482c.jpg"},
        { src: "http://susgtyiom.hb-bkt.clouddn.com/20250421/photo/56_6cb38c3683d039f0c6ec180c0cccb3c.jpg"},
        { src: "http://susgtyiom.hb-bkt.clouddn.com/20250421/photo/61_27adeb2526638e0877d0f00fde23579.jpg"},
        { src: "http://susgtyiom.hb-bkt.clouddn.com/20250421/photo/64_34f1c97154fd3aac9b0fff7ef822760.jpg"},



      ],
      quotes: [
        "Talk is cheap, show me the code.",
        "Code never lies, comments sometimes do.",
        "First, solve the problem. Then, write the code.",
        "In order to be irreplaceable, one must always be different.",
        "The only way to learn a new programming language is by writing programs in it.",
        "Programming isn't about what you know; it's about what you can figure out.",
        "A good programmer is someone who always looks both ways before crossing a one-way street.",
        "Code is like humor. When you have to explain it, it’s bad.",
        "Simplicity is the soul of efficiency.",
        "Software is a great combination of artistry and engineering.",
        "La programación no es difícil, es solo lógica.", // Spanish: Programming is not hard, it's just logic.
        "Quem sabe, faz. Quem não sabe, ensina.", // Portuguese: Those who know, do. Those who don't, teach.
        "Le code est le reflet de la pensée humaine.", // French: Code is the reflection of human thought.
        "コードは思考の反映です。", // Japanese: Code is the reflection of thought.
        "El código nunca miente, pero las explicaciones sí.", // Spanish: Code never lies, but explanations do.
        "La simplicité est la clé de l'efficacité.", // French: Simplicity is the key to efficiency.
        "Programa en el camino, no en la teoría.", // Spanish: Program on the way, not in theory.
        "La informática no es solo saber, es aprender a aprender.", // Spanish: Computer science is not just knowing, it's learning how to learn.
        "A program should be easy to read and easy to debug.", // English
        "Usa la fuerza, pero hazlo de forma eficiente.", // Spanish: Use the force, but do it efficiently.
        "Good code is its own documentation.", // English
        "Cada línea de código es una oportunidad para mejorar.", // Spanish: Every line of code is an opportunity to improve.
        "El código no miente.", // Spanish: Code does not lie.
        "在编程中，时间是最宝贵的资源。", // Chinese: Time is the most valuable resource in programming.
        "Code is like a mirror; it reflects what you put in.", // English
        "La informática es el arte de hacer que las cosas que quieres sucedan.", // Spanish: Computer science is the art of making the things you want happen.
        "Les erreurs de programmation sont les meilleures professeurs.", // French: Programming errors are the best teachers.
        "自学是程序员最强大的武器。", // Chinese: Self-study is the programmer's strongest weapon.
        "El éxito en programación no es hacer todo bien, sino hacer todo funcional.", // Spanish: Success in programming is not about doing everything right, but making everything work.
        "一行代码，一段人生。", // Chinese: A line of code, a chapter of life.
        "程序员就像魔术师，他们能变出奇迹。", // Chinese: Programmers are like magicians, they can create miracles.
        "El código es poesía para las máquinas.", // Spanish: Code is poetry for machines.
        "Un buen programador es aquel que sabe lo que hace sin tener que preguntárselo.", // Spanish: A good programmer is someone who knows what they are doing without asking.
        "Crear un buen código es una forma de arte.", // Spanish: Creating good code is a form of art.
        "La programación es la poesía de las matemáticas.", // Spanish: Programming is the poetry of mathematics.
        "Programación es resolver problemas con lógica.", // Spanish: Programming is solving problems with logic.
        "La programación no es solo una habilidad técnica, sino una forma de pensar.", // Spanish: Programming is not just a technical skill, but a way of thinking.
        "El código es el camino hacia la verdad en el mundo digital.", // Spanish: Code is the path to truth in the digital world.
        "In coding, mistakes are not failures, they are learning opportunities.", // English
        "Good programmers are those who can write code that is easy to read.", // English
        "The best programs are those that are written with the user's needs in mind.", // English
        "Code can be simple but elegant, and that’s the beauty of programming.", // English
        "Le code est la poésie des machines.", // French: Code is the poetry of machines.
        "La tecnología solo funciona si la gente sabe cómo usarla.", // Spanish: Technology only works if people know how to use it.
        "Don’t write code, write solutions.", // English
        "In programming, you don’t just learn a language, you learn how to think.", // English
        "Por cada problema, hay una solución elegante en el código.", // Spanish: For every problem, there is an elegant solution in code.
        "Créer du code, c'est façonner l'avenir.", // French: Creating code is shaping the future.
        "The hardest part of programming is deciding what to build.", // English
        "A computer program does what you tell it to do, not what you want it to do.", // English
        "The best way to predict the future is to invent it.", // English
        "Abstraction is the art of simplifying complexity.", // English
        "Un buen programador es aquel que puede escribir código fácil de leer.", // Spanish: A good programmer is one who can write easy-to-read code.
        "Nunca dejes que tu código te controle. Sé tú quien controle el código.", // Spanish: Never let your code control you. Be the one who controls the code.
        "In programming, no solution is perfect, but every solution can be improved.", // English
        "El código limpio es el mejor código.", // Spanish: Clean code is the best code.
        "El código es un medio para lograr grandes cosas.", // Spanish: Code is a means to achieve great things.
        "A good algorithm is the soul of any program.", // English
        "Nunca dejes de aprender, porque el código siempre está evolucionando.", // Spanish: Never stop learning, because code is always evolving.
        "L'informatique est la science qui rend l'impossible possible.", // French: Computer science is the science that makes the impossible possible.
        "En programación, lo simple es a menudo lo mejor.", // Spanish: In programming, simplicity is often the best.
        "Code is like a recipe. You can’t skip steps.", // English
        "Le code est une façon d'exprimer l'impossible de manière possible.", // French: Code is a way of expressing the impossible in a possible way.
        "Coding is not just about syntax, it's about problem-solving.", // English
        "Cuando el código se vuelve poesía, el programador se convierte en artista.", // Spanish: When code becomes poetry, the programmer becomes an artist.
        "No hay límites en la programación, solo las reglas de la lógica.", // Spanish: There are no limits in programming, only the rules of logic.
        "Un error en el código es solo una oportunidad para mejorar.", // Spanish: An error in the code is just an opportunity to improve.
        "Programming is the art of making the impossible, possible.", // English
        "Un código limpio es un código legible.", // Spanish: Clean code is readable code.
        "La programación es el arte de transformar ideas en realidad digital.", // Spanish: Programming is the art of turning ideas into digital reality.
        "El verdadero poder de un programador no radica en saber mucho, sino en saber qué hacer con lo que sabe.", // Spanish: The true power of a programmer doesn't lie in knowing a lot, but in knowing what to do with what they know.
        "A program without a plan is like a ship without a captain.", // English
        "Programmer's job is to create value through code.", // English
        "Cuando escribas código, piensa como un arquitecto, no como un albañil.", // Spanish: When you write code, think like an architect, not a builder.
        "Programming is a tool, not a job.", // English
        "A developer is someone who gets things done, not just a coder.", // English
        "El código es como la música: se debe sentir bien, no solo ser correcto.", // Spanish: Code is like music: it should feel good, not just be correct.
        "Every program is a story waiting to be told.", // English
        "Don’t repeat yourself (DRY principle).", // English
        "A good programmer writes code that others can read.", // English
        "Life is too short to write bad code.", // English
        "El buen código es como la poesía; tiene que fluir.", // Spanish: Good code is like poetry; it has to flow.
        "La programación es como un juego de rompecabezas que nunca termina.", // Spanish: Programming is like a puzzle game that never ends.
        "The best way to improve your programming skills is to write a lot of code.", // English
        "La programación no es solo escribir código, es hacer que el mundo sea mejor.", // Spanish: Programming is not just about writing code, it's about making the world better.
        "El código sin pruebas es como un libro sin índice.", // Spanish: Code without tests is like a book without an index.
        "An optimized program is one that is easy to maintain.", // English
        "In programming, failure is an opportunity to improve.", // English
        "La programación es un arte donde cada línea de código cuenta.", // Spanish: Programming is an art where every line of code matters.
        "Write code as if the person who will maintain it is a violent psychopath who knows where you live.", // English
        "El código limpio es la mejor forma de asegurar que otros puedan entender tu trabajo.", // Spanish: Clean code is the best way to ensure others can understand your work.
        "Don't just solve the problem, solve it the right way.", // English
        "La programación es resolver problemas de forma creativa.", // Spanish: Programming is solving problems creatively.
        "The key to successful programming is perseverance.", // English
        "Cada línea de código tiene el potencial de cambiar el mundo.", // Spanish: Every line of code has the potential to change the world.
        "Coding is like building a house. If the foundation is weak, the rest will crumble.", // English
        "La creatividad y la lógica deben trabajar juntas en la programación.", // Spanish: Creativity and logic must work together in programming.
        "El programador que no entiende su código es un programador perdido.", // Spanish: A programmer who doesn't understand their code is a lost programmer.
        "Code should be written to last, not to just work.", // English
        "Learning to code is learning to think differently.", // English
        "No hay atajos en la programación, solo resultados", // Spanish: There are no shortcuts in programming, only results.
        "代码是写给人看的，计算机只是运行它。",
        "没有错误的代码是一种奢望，只有更好的错误处理。",
        "程序员的使命是将不可能变为可能。",
        "编程的乐趣在于解决问题的过程，而不是结果。",
        "代码就像诗歌，简单而优雅。",
        "一个优秀的程序员是不会让程序崩溃的人。",
        "代码就像咖啡，少了它，生活都不完整。",
        "程序员最大的优势是善于从失败中汲取经验。",
        "要么写出简单的代码，要么写出能让别人理解的代码。",
        "没有一个程序员能一开始就写出完美的代码。",
        "代码质量是最重要的，而不是写多少行代码。",
        "写代码的最佳方式是以一种你自己能够理解的方式写。",
        "算法不等于程序，程序员不仅要懂算法，还要懂如何用代码实现它。",
        "编程是一场永无止境的挑战，永远不会停止学习。",
        "好的程序员懂得如何避免复杂性，简洁才是王道。",
        "当你写下第一行代码时，你已经准备好接受挑战。",
        "错误总是在程序里藏匿，优秀的程序员是能找到并解决它的人。",
        "程序员不仅仅是写代码，更是在实现创造。",
        "编程是解决问题的艺术，而不是完成任务。",
        "没有完美的代码，只有能改进的代码。",
        "编程就是对问题的不断抽象和解决。",
        "代码的质量决定了程序的生命力。",
        "重构是一种艺术，它不仅仅是改进代码，更是让它焕然一新。",
        "每一行代码背后都藏着一个故事。",
        "最好的程序员是那些能与其他人一起解决问题的人。",
        "编程的意义不仅仅是解决眼前的问题，更是在为未来铺路。",
        "不做重复的事，写高效的代码。",
        "好程序员的秘诀就是坚持不懈地优化和重构代码。",
        "每写一行代码，都要为自己留下足够的注释。",
        "编程不仅仅是思考如何写代码，更是思考如何让代码运行更高效。",
        "程序员是可以改变世界的人，代码是他们的武器。",
        "编程是一种逻辑思维的训练，它教会你如何抽象和优化问题。",
        "代码质量很重要，但代码的可读性更重要。",
        "编程不仅仅是完成任务，而是如何解决问题。",
        "无论何时，都要保持对编程的热爱和耐心。",
        "每写一行代码，都要为它可能带来的影响负责。",
        "程序员不仅是技术人员，也是创新者。",
        "优秀的程序员是那些能在复杂中找到简洁解法的人。",
        "写代码的时候要想清楚，不要让代码变得凌乱不堪。",
        "编程是对抗未知的勇气，是不断发现问题并解决的过程。",
        "代码的美是有结构和整洁的。",
        "在编程中，追求完美可能会让你停滞不前，重要的是完成并不断改进。",
        "编程不仅是工具，更是一种表达思想的方式。",
        "每个程序员都有自己的编程哲学，但最好的编程哲学是清晰简洁。",
        "做一个优秀的程序员，先学会如何解决问题。",
        "编程是逻辑思维的训练，解决问题时保持冷静。",
        "在编程中，错误是最好的老师。",
        "编程就像拆解问题，每一步都需要仔细思考。",
        "代码越简洁，错误越少。",
        "最好的程序员不是最快写代码的人，而是最能解决问题的人。",
        "让代码变得简单，是程序员的最高境界。",
        "写代码就像修理一台机器，要时刻关注每一个细节。",
        "每一行代码都可能是你进步的关键。",
        "编程是对抽象问题的最优解法。",
        "没有不出错的代码，只有更高效的错误处理。",
        "程序员的核心技能是不断学习和解决新问题。",
        "一个程序员的成长不是在技术上，而是在解决问题的能力上。",
        "不断地编写和优化代码，是成为高手的必经之路。",
        "编程的艺术就是简化复杂的问题。",
        "优秀的代码背后，是清晰的思维和高效的解决方案。",
        "写代码要从最简单的思考方式出发，再逐步优化。",
        "编程不仅仅是任务的完成，更是对未知问题的挑战。",
        "写代码就像在塑造一件艺术品，需要反复雕琢。",
        "编程是一种持续探索的过程，永无止境。",
        "优秀的程序员能够将复杂的代码结构化并简化。",
        "重构是一种艺术，它让代码变得更加高效与简洁。",
        "程序员要具备极强的耐心和细致的思维。",
        "不要怕犯错误，每次错误都会让你更强大。",
        "代码就是要让别人理解，你自己也能理解。",
        "优秀的程序员懂得如何在简单和高效之间找到平衡。",
        "编程不仅仅是技术的挑战，更是思维的挑战。",
        "程序员的工作不仅是写代码，还要保持代码的可读性。",
        "代码是沟通的语言，它不仅是给机器看的，也是给人看的。",
        "代码的简洁程度决定了它的效率。",
        "编程最重要的技能是解决问题的能力。",
        "一个好的程序员懂得如何在有限的时间内完成最好的工作。",
        "写代码时，注重细节是避免出错的关键。",
        "代码没有最优解，只有适合当前问题的解决方案。",
        "编程是用一种不言语的方式来表达思想。",
        "一个高效的程序员不仅能写出高效的代码，还能写出清晰易懂的代码。",
        "代码的优雅来自于简洁而高效的设计。",
        "程序员需要面对的是不断变化的挑战，解决问题才是最重要的。",
        "没有永远不出错的代码，只有持续改进的代码。",
        "编程是解决问题的一种方式，不是为了展示技巧。",
        "当你能解决一个复杂的问题时，你就能掌控它。",
        "写代码不仅要想着如何做得快，更要想着做得好。",
        "不要依赖于框架，学习编程的核心思想。",
        "编程的精髓在于反复的调试和优化。",
        "一个好的程序员会提前想到问题，而不是事后去处理错误。",
        "编程就像雕刻，每一次修改都在让作品更加完美。",
        "写代码时，时刻保持高效和清晰的思维。",
        "编程不是仅仅为了完成任务，而是为了解决问题。",
        "在编程时要学会保持冷静，做出理智的决定。",
        "要在编程的过程中不断提高自己的思维能力和问题解决能力。",
        "代码的设计不仅要简洁，还要能够承受未来的扩展。",
        "写代码时，每一行都应该有其明确的目的。",
        "编程是一种持续进步的过程，不断的总结和反思会帮助你成长。",
        "解决问题的过程就是编程的乐趣所在。",
        "每个程序员都在不断的学习过程中变得更强大。",
        "优秀的代码并不复杂，而是简单明了且易于维护。",
        "在编程的道路上，永远不要停止前进。",
        "最好的程序员是那些能在复杂中看到简单的人。",
        "代码就是计算机的语言，也是人类思想的表达。",
        "优秀的程序员不会写一堆废话，而是直接进入问题的核心。",
        "编程不仅仅是解决问题，更多的是发现问题并提出解决方案。",
        "编程是一项不断探索与创新的工作。",
        "每一次调试都会使你对编程的理解更加深刻。",
        "写代码要遵循原则，而不是一味追求速度。",
        "程序员的最大挑战是如何在复杂的系统中找到简洁的解决方案。",
        "在编程的过程中，每次找到一个解决方案，都会带来一种成就感。",
        "编程的过程中要保持严谨，任何小的错误都会影响最终结果。",
        "程序员的职责不仅是完成任务，更要提供最优的解决方案。",
        "解决问题时，先找出最简单的方法，然后逐步优化。",
        "每一次重构都可以让代码变得更加高效。",
        "优秀的程序员懂得如何保持代码的高效性与可读性。",
        "一个优秀的程序员不仅能编写代码，还能维护和优化代码。",
        "编程是一种习惯，编写清晰代码是每个程序员的责任。",
        "优秀的程序员会不断挑战自己，在困难中寻找突破口。",
        "编程不只是一项技术，更是一种思维方式。",
        "编程是通向解决问题的桥梁。",
        "编程的核心不在于语言本身，而在于如何使用它来解决问题。",
        "写代码时要考虑到维护性，长远的优化才是最重要的。",
        "优秀的程序员懂得如何从错误中学习，而不是重复错误。",
        "编程不仅是构建功能，而是优化每个细节。",
        "编程就像一场冒险，每一次突破都会让你更强。",
        "每一行代码都有其独特的意义和价值。",
        "在编程中，不仅要考虑如何实现功能，还要考虑如何优化性能。",
        "解决问题时，不要急于出结果，要有耐心和思考。",
        "编程的过程是学习和实践相结合的过程。",
        "写代码时要懂得如何简化每一个步骤，追求高效与简洁。",
        "优秀的程序员会充分考虑代码的可扩展性和可维护性。",
        "每一行代码背后都有一个逻辑，而程序员要学会理解这些逻辑。",
        "编程是一个不断挑战自己并从中获得进步的过程。",
        "写代码时要有全局观念，考虑到未来的可扩展性。",
        "每一次改进代码，都是让程序更接近完美的一步。",
        "编程就是为了解决实际问题，不能停留在理论中。",
        "优秀的程序员不仅仅是写代码，更是解决问题的高手。",
        "写代码的乐趣在于从无到有的创造过程。",
        "每一次编程，都有机会提升自己的思维能力。",
        "编程不仅仅是写程序，更是解决问题的一种方式。",
        "每一次调试，都是编程过程中的一次学习机会。",
        "学会编程，学会如何将想法变为现实。",
        "在编程的世界里，解决问题的能力比写出完美代码更重要。",
        "写代码时要学会用最简洁的方式表达复杂的逻辑。",
        "程序员的责任不仅是写代码，更要让代码能够运行在现实中。",
        "每一次错误的背后，都是一次深刻的学习经历。",
        "编程是一种习惯，优秀的程序员总是能在每次迭代中进步。",
        "优秀的程序员懂得如何在复杂的系统中找到简单的解决方案。",
        "编程的核心在于不断优化和重构，不断提高效率和可读性。",
        "每一次成功的编程，都能为你带来成就感。",
        "写代码是一种挑战，但解决问题的过程更让人激动。",
        "代码不仅仅是计算机的语言，更是思考和表达的工具。",
        "编程的乐趣不仅在于结果，更在于过程中发现的问题和解决方案。",
        "编程不仅仅是完成任务，它是实现创意和解决实际问题的一种方式。",
        "程序员的每一行代码背后，都是对问题的深刻理解。",
        "编程是一种力量，它能改变世界。",
        "编程不仅是技能，更是一种艺术。",
        "真正的程序员不仅仅是写代码的人，还是优化和重构代码的人。",
        "编程是最直接的创造，不断优化是成为优秀程序员的关键。",
        "学会反思自己的代码，这是程序员成长的重要一步。",
        "每次解决一个问题，都会成为更好的程序员。",
        "代码中没有永远不变的解决方案，只有更好的解决方案。",
        "成功的程序员不仅要会编程，更要懂得如何解决实际问题。",
        "写代码的时候，要清楚每一行代码的目的。",
        "编程是一种不断摸索的过程，但每一次成功都值得庆祝。",
        "程序员的工作不止是完成任务，更是不断挑战极限。",
        "只有不断挑战自己，才能成为更优秀的程序员。",
        "编程的魅力在于它让你发现并解决一个个看似无解的问题。",
        "代码永远不会完美，但总能找到更好的解决方法。",
        "编程不是最终目的，而是解决问题的工具。",
        "程序员是一个持续学习者，永远不会停止提升自己。",
        "学会写测试代码，这是做一个好程序员的基础。",
        "优秀的代码不仅能解决问题，还能避免未来的问题。",
        "编程需要清晰的思维和简洁的表达。",
        "写代码就像写诗，每个字符都在表达思想。",
        "Talk is cheap, show me the code.",
        "Code never lies, comments sometimes do.",
        "First, solve the problem. Then, write the code.",
        "In order to be irreplaceable, one must always be different.",
        "The only way to learn a new programming language is by writing programs in it.",
        "Programming isn't about what you know; it's about what you can figure out.",
        "A good programmer is someone who always looks both ways before crossing a one-way street.",
        "Code is like humor. When you have to explain it, it’s bad.",
        "Simplicity is the soul of efficiency.",
        "Software is a great combination of artistry and engineering."
      ],
      currentQuote: "",
      showPreview: false,
      previewImage: ''
    };
  },
  mounted() {
    this.loadQuiz();

    this.changeQuote();  // 初始化时展示一条语录
    // 设置年龄
    const birthYear = 2005;
    const currentYear = new Date().getFullYear();
    const age = currentYear - birthYear;
    document.getElementById('age').textContent = age;

    // 监听滚动
    window.addEventListener('scroll', this.checkScroll);

    // 启动时间刷新
    this.updateTime();
    setInterval(this.updateTime, 1000);

    // 生成程序员身份
    this.generateProgrammerTitle();
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.checkScroll);
  },
  methods: {
    changeQuote() {
      const randomIndex = Math.floor(Math.random() * this.quotes.length);
      this.currentQuote = this.quotes[randomIndex];
    },
    loadQuiz() {
      const index = Math.floor(Math.random() * this.quizData.length);
      this.currentQuiz = this.quizData[index];
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
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    updateTime() {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString();
    },
    generateProgrammerTitle() {
      const titles = [
        "bug猎人", "全栈忍者", "注释大师", "键盘诗人", "算法冒险家",
        "需求扼杀者", "代码炼金术士", "Git时间旅行者", "调试神仙", "数据狂人",
        "异步大师", "正则魔法师", "代码大师", "前端女巫", "后端霸主",
        "框架战士", "数据库达人", "界面设计师", "测试忍者", "服务器守护者",
        "性能优化专家", "UI设计大神", "CSS魔术师", "React战士", "Vue侠",
        "Node.js狂人", "Python巫师", "Java超人", "GitHub征服者", "Cloud守望者",
        "数据科学术士", "机器学习大师", "人工智能专家", "深度学习勇士", "算法破坏者",
        "黑客帝国入侵者", "编程黑客", "代码铁匠", "分布式系统指挥官", "RESTful传教士",
        "Docker狂人", "虚拟机驾驶员", "云计算先锋", "前端炼金术士", "算法工程师",
        "技术狂人", "编程哲学家", "函数式编程大师", "IDE控制者", "代码行走者",
        "代码漫游者", "数据可视化艺术家", "敏捷开发大使", "版本控制高手", "bug终结者",
        "数据驱动决策者", "自动化大师", "分布式架构专家", "技术无限探索者", "编程实践者"
      ];

      this.programmerTitle = titles[Math.floor(Math.random() * titles.length)];
    },

    openPreview(imgUrl) {
      this.previewImage = imgUrl;
      this.showPreview = true;
    },
    closePreview() {
      this.showPreview = false;
    }
  }
};
</script>


<style lang="scss" scoped>
.quote-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 50px;
}

.quote-text {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #333;
}

.change-quote-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.change-quote-button:hover {
  background-color: #45a049;
}
.about-page {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.about-card {
  max-width: 1000px;
  width: 100%;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  line-height: 1.8;
  color: #7a7979;

  section {
    margin-top: 2rem;
  }

  h1 {
    margin-bottom: 0.5rem;
    font-size: 2rem;
  }
  .photo-gallery {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .photo-thumb {
    width: 300px;
    height: auto;
    object-fit: cover;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.3s;
  }
  .photo-thumb:hover {
    transform: scale(1.05);
  }
  .preview-mask {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
  }
  .preview-img {
    max-width: 90%;
    max-height: 80%;
    border-radius: 10px;
  }

  h2 {
    position: relative;
    margin-top: 1.5rem;
    font-size: 1.5rem;
    color: #007acc;

    &::after {
      content: '';
      display: block;
      width: 60px;
      height: 4px;
      background-color: #007acc;
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
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      margin-right: 2rem;
    }

    .intro-text {
      flex: 1;
      .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin: 0.5rem 0 1rem;
      }
    }
  }

  .section-image {
    width: 100%;
    height: auto;
    margin-top: 1rem;
    border-radius: 8px;
  }

  .progress-bar {
    background-color: #e0e0e0;
    border-radius: 8px;
    height: 8px;
    margin: 5px 0;
  }

  .progress {
    background-color: #4caf50;
    height: 100%;
    border-radius: 8px;
  }

  .back-to-top {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background-color: #007acc;
    color: white;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    font-size: 1.5rem;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #005fa3;
    }
  }
}
</style>
