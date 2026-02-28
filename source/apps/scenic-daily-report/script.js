// 更新时间显示
function updateLastUpdateTime() {
    const now = new Date();
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    document.getElementById('lastUpdate').textContent = now.toLocaleDateString('zh-CN', options);
}

// 获取新闻数据
async function fetchNews() {
    try {
        // 实际新闻数据
        const newsData = {
            topNews: [
                {
                    title: "Boss直聘崩了",
                    url: "https://www.baidu.com/s?ie=UTF-8&wd=Boss%E7%9B%B4%E8%81%98%E5%B4%A9%E4%BA%86",
                    source: "百度热点",
                    heat: "790.7万"
                },
                {
                    title: "李嘉诚卖港口 香港两任特首都发声了",
                    url: "https://www.baidu.com/s?ie=UTF-8&wd=%E6%9D%8E%E5%98%89%E8%AF%9A%E5%8D%96%E6%B8%AF%E5%8F%A3",
                    source: "百度热点",
                    heat: "787.5万"
                },
                {
                    title: "让钱包鼓起来、消费旺起来",
                    url: "https://www.baidu.com/s?ie=UTF-8&wd=%E8%AE%A9%E9%92%B1%E5%8C%85%E9%BC%93%E8%B5%B7%E6%9D%A5",
                    source: "百度热点",
                    heat: "778.5万"
                },
                {
                    title: "海底捞顾客拒与同桌人平分赔偿金",
                    url: "https://www.baidu.com/s?ie=UTF-8&wd=%E6%B5%B7%E5%BA%95%E6%8D%9E%E9%A1%BE%E5%AE%A2%E6%8B%92%E4%B8%8E%E5%90%8C%E6%A1%8C%E4%BA%BA%E5%B9%B3%E5%88%86%E8%B5%94%E5%81%BF%E9%87%91",
                    source: "百度热点",
                    heat: "762.6万"
                },
                {
                    title: "小米汽车单台平均亏损4.5万元",
                    url: "https://www.baidu.com/s?ie=UTF-8&wd=%E5%B0%8F%E7%B1%B3%E6%B1%BD%E8%BD%A6%E5%8D%95%E5%8F%B0%E5%B9%B3%E5%9D%87%E4%BA%8F%E6%8D%9F4.5%E4%B8%87%E5%85%83",
                    source: "百度热点",
                    heat: "753.1万"
                }
            ],
            hotTopics: [
                {
                    title: "成都辟谣艾滋病17万人",
                    url: "https://s.weibo.com/weibo?q=%23%E6%88%90%E9%83%BD%E8%BE%9F%E8%B0%A3%E8%89%BE%E6%BB%8B%E7%97%8517%E4%B8%87%E4%BA%BA%23",
                    source: "微博热搜",
                    heat: "118.4万"
                },
                {
                    title: "乘风2025全阵容官宣",
                    url: "https://s.weibo.com/weibo?q=%23%E4%B9%98%E9%A3%8E2025%E5%85%A8%E9%98%B5%E5%AE%B9%E5%AE%98%E5%AE%A3%23",
                    source: "微博热搜",
                    heat: "99.6万"
                },
                {
                    title: "网友称请朋友吃海底捞遇「小便门」",
                    url: "https://www.zhihu.com/question/15287718851",
                    source: "知乎热榜",
                    heat: "1053万"
                },
                {
                    title: "大象产肉量是猪的20倍，为什么不养大象来吃？",
                    url: "https://www.zhihu.com/question/15175830276",
                    source: "知乎热榜",
                    heat: "515万"
                },
                {
                    title: "上海黄浦区对8岁以下禁售「二次元」商品",
                    url: "https://www.zhihu.com/question/15268492296",
                    source: "知乎热榜",
                    heat: "431万"
                }
            ]
        };
        
        return newsData;
    } catch (error) {
        console.error('获取新闻数据失败:', error);
        return null;
    }
}

// 渲染新闻列表
function renderNews(data) {
    const topNewsContainer = document.getElementById('topNews');
    const hotTopicsContainer = document.getElementById('hotTopics');
    
    // 清空现有内容
    topNewsContainer.innerHTML = '';
    hotTopicsContainer.innerHTML = '';
    
    // 渲染头条新闻
    data.topNews.forEach(news => {
        const newsElement = createNewsElement(news);
        topNewsContainer.appendChild(newsElement);
    });
    
    // 渲染热门话题
    data.hotTopics.forEach(topic => {
        const topicElement = createNewsElement(topic);
        hotTopicsContainer.appendChild(topicElement);
    });
}

// 创建新闻元素
function createNewsElement(news) {
    const div = document.createElement('div');
    div.className = 'news-item';
    
    div.innerHTML = `
        <a href="${news.url}" target="_blank">
            <div class="news-title">${news.title}</div>
            <div class="source">来源：${news.source}</div>
            <div class="heat">热度：${news.heat}</div>
        </a>
    `;
    
    return div;
}

// 初始化页面
async function initializePage() {
    updateLastUpdateTime();
    const newsData = await fetchNews();
    if (newsData) {
        renderNews(newsData);
    }
}

// 定时刷新数据（每5分钟）
function setupAutoRefresh() {
    setInterval(async () => {
        const newsData = await fetchNews();
        if (newsData) {
            renderNews(newsData);
            updateLastUpdateTime();
        }
    }, 5 * 60 * 1000);
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    initializePage();
    setupAutoRefresh();
}); 