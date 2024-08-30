
var link = "/articles/coursea/24lectures/intro/"
var img = "https://images.jieyu.ai/images/hot/course_promotion.jpg"
excludes = ["/articles/coursea", "/articles/python/best-practice-python"]

var ad = [
    '<div class="admonition tip">',
    '<style>',
    '    ol>li {',
    '        font-size: 12px;',
    '        margin: 0;',
    '        line-height: 1.2rem;',
    '    }',
    '</style>',
    '<p class="admonition-title">《因子投资与机器学习策略》喊你上课啦！</p>',
    '<p>面向策略研究员的专业课程，涵盖<b>因子挖掘</b>、<b>因子检验</b>和基于<b>机器学习</b>的策略开发三大模块，构建你的个人竞争优势！</p>',
    '<ol>',
    '<div style="text-align:center;width:120px;float:right;margin-top:-20px">',
    '<img src="https://images.jieyu.ai/images/hot/quantfans.png"/>',
    '<span>课程助教: 宽粉</span>',
    '</div>',
    '<li>全网独家精讲 Alphalens 分析报告，助你精通因子检验和调优。</li>',
    '<li>超 400 个独立因子，分类精讲底层逻辑，学完带走 350+ 因子实现。</li>',
    '<li>课程核心价值观：Learning without thought is labor lost. Know-How & Know-Why.</li>',
    '<li>三大<b>实用模型</b>，奠定未来研究框架<sup>1</sup>：聚类算法寻找配对交易标的（中性策略核心）、基于 XGBoost 的资产定价、趋势交易模型。</li>',
    '<li>领先教学手段：SBP（Slidev Based Presentation）、INI（In-place Notebook Interaction）和基于 Nbgrader（UCBerkley 使用中）的作业系统。</li>',
    '</ol>',
    '<hr style="border-bottom:1px solid #ccc;height:1px;width:20%">',
    '<p style="font-size:10px !important">1. 示例模型思路新颖。未来一段时间，你都可以围绕这些模型增加因子、优化参数，构建出领先的量化策略系统。</p>',
    '</div>'
].join("\n")

function insertAd(minParas, minWords) {
    // 如果地址在exclude目录中，则不插入广告
    for (i = 0; i < excludes.length; i++) {
        if (location.pathname.indexOf(excludes[i]) == 0) {
            return
        }
    }
    // 如果已经包含了链接，则不再增加，以允许手动增加
    var links = document.querySelectorAll("a[href*='" + link + "']");
    if (links.length > 2) {//菜单栏总是包含对此链接的引用
        console.log("已添加")
        return
    }

    // var ad = "<p><a href='" + link + "'target='_blank'>" + "<img src='" + img + "'/>" + "</p>"

    var paras = document.querySelectorAll("article p");
    var wordCount = 0
    var paraCount = 0
    var inserted = 0
    for (var i = 0; i < paras.length; i++) {
        var p = paras[i];
        paraCount++
        wordCount += p.innerText.length
        if (inserted >= 2) {
            break
        }

        if (paraCount >= minParas && wordCount >= minWords) {
            console.log("find para", p, paraCount, wordCount)
            p.insertAdjacentHTML("afterend", ad)
            paraCount = 0
            wordCount = 0
            inserted += 1
        }
    }
    if (inserted == 0 & paras.length >= 5) {
        var article = document.getElementsByTagName("article")[0]
        article.insertAdjacentHTML("beforeend", ad)
    }
}

document$.subscribe(function () {
    console.log("call in ad")
    insertAd(40, 4000)
    // fetch("/assets/ad/ad.txt").then(response =>{
    //     return response.text()
    // }).then(ad =>{
    //     insertAd(ad, 30, 3000);
    // })
})
