
var link="/articles/coursea/24lectures/intro/"
var img = "https://images.jieyu.ai/images/hot/course_promotion.jpg"

var ad = [
    '\n\n<div class="admonition tip">',
        '<p class="admonition-title">',
            '现在报名量化课程，立享优惠！',
        '</p>',
        '<p></p>',
        '<div style="width:180px; position: relative;float:right;top:20px;right:-10px">',
        '<img src="https://images.jieyu.ai/images/hot/quantfans.png" style="width: 150px; display:inline-block;">',
        '<p style="text-align:center;width:150px;margin-top:-10px"> 课程助教: 宽粉 </p>',
        '</div>',
        '<p>包含视频、Notebook文稿、代码和每周一次答疑。文字稿约40万字节。课程提供实验环境和商业数据</p>',
        '<ul>',
        '<li>Jupyter Lab策略研究环境，无须学员安装</li>',
        '<li>超过30亿条分钟级行情数据，盘中实时更新</li>',
        '<li>真实生产环境，有回测服务</li>',
        '<li>192核CPU和256GB内存</li>',
        '<li>免费送 Zillionare 量化框架</li>',
        '</ul>',
    '</div>'
].join('\n')

function insertAd(minParas, minWords){
    // 如果已经包含了链接，则不再增加，以允许手动增加
    var links = document.querySelectorAll("a[href*='" + link + "']");
    if (links.length > 0){
        console.log("已添加")
        return
    }

    // var ad = "<p><a href='" + link + "'target='_blank'>" + "<img src='" + img + "'/>" + "</p>"

    var paras = document.querySelectorAll("article p");
    var wordCount = 0
    var paraCount = 0
    var inserted = 0
    for (var i = 0; i < paras.length; i++){
        var p = paras[i];
        paraCount ++
        wordCount += p.innerText.length
        if (inserted >= 2){
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
    if (inserted == 0 & paras.length >= 5){
        var article = document.getElementsByTagName("article")[0]
        article.insertAdjacentHTML("beforeend", ad)
    }
}

document$.subscribe(function() {
    console.log("call in ad")
    insertAd(40, 4000)
    // fetch("/assets/ad/ad.txt").then(response =>{
    //     return response.text()
    // }).then(ad =>{
    //     insertAd(ad, 30, 3000);
    // })
})
