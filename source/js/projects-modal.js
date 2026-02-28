// 项目数据
const projectsData = [
  {
    title: '投资收益率（汇报版）',
    date: '2025-02-27',
    excerpt: '投资收益率计算工具，汇报版',
    demo: '/apps/investment-roi/',
    download: null,
    tags: ['工具']
  },
  {
    title: 'HealthLog Mobile',
    date: '2025-02-27',
    excerpt: 'HealthLog 离线移动应用（下载版）',
    demo: null,
    download: '/downloads/healthlog-mobile.zip',
    tags: ['移动端', 'Expo']
  },
  {
    title: '方针管理 1.6',
    date: '2025-02-27',
    excerpt: '方针管理系统 1.6 版本（下载版）',
    demo: null,
    download: '/downloads/policy-management-1-6.zip',
    tags: ['管理']
  },
  {
    title: 'expfood-mvp',
    date: '2025-02-27',
    excerpt: 'expfood-mvp 项目',
    demo: '/apps/expfood-mvp/',
    download: '/downloads/expfood-mvp.tar.gz',
    tags: ['工具']
  },
  {
    title: 'juben',
    date: '2025-02-27',
    excerpt: '剧本项目',
    demo: '/apps/juben/',
    download: '/downloads/juben.tar.gz',
    tags: ['工具']
  },
  {
    title: '利润差异分析',
    date: '2025-02-28',
    excerpt: '财务利润差因素拆解工具',
    demo: '/apps/profit-difference-analysis/',
    download: '/downloads/profit-difference-analysis.zip',
    tags: ['财务', '分析']
  },
  {
    title: '景点日报',
    date: '2025-02-28',
    excerpt: '伊犁那拉提景区日报静态展示页',
    demo: '/apps/scenic-daily-report/',
    download: '/downloads/scenic-daily-report.zip',
    tags: ['文旅', '日报', '可视化']
  },
  {
    title: 'SIC经营指标监控',
    date: '2025-02-28',
    excerpt: 'VPO 工作站经营指标多维看板',
    demo: '/apps/sic-kpi-monitor/',
    download: '/downloads/sic-kpi-monitor.zip',
    tags: ['看板', '监控', '经营分析']
  },
  {
    title: '音乐节拍器',
    date: '2025-02-28',
    excerpt: '音乐节奏练习工具（下载版）',
    demo: null,
    download: '/downloads/音乐节拍器.zip',
    tags: ['工具']
  },
  {
    title: '粒子显示',
    date: '2025-02-28',
    excerpt: 'Canvas 粒子动画效果展示',
    demo: '/apps/粒子显示/',
    download: '/downloads/粒子显示.zip',
    tags: ['可视化']
  }
];

// 打开模态框
function openProjectsModal() {
  const modal = document.getElementById('projects-modal');
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

// 关闭模态框
function closeProjectsModal() {
  const modal = document.getElementById('projects-modal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
}

// 渲染项目卡片
function renderProjects() {
  const container = document.getElementById('projects-grid');
  if (!container) return;

  container.innerHTML = projectsData.map(project => `
    <div class="project-card-modal">
      <h3>
        <a href="${project.demo || '#'}" ${project.demo ? 'target="_blank"' : ''}>${project.title}</a>
      </h3>
      <p class="project-meta">${project.date}</p>
      <p class="project-excerpt">${project.excerpt}</p>
      <div class="project-actions">
        ${project.demo ? `<a class="btn-modal btn-demo" href="${project.demo}" target="_blank">在线体验</a>` : ''}
        ${project.download ? `<a class="btn-modal btn-download" href="${project.download}" target="_blank">下载源码</a>` : ''}
      </div>
      ${project.tags ? `<p class="project-tags">${project.tags.map(tag => `<span>#${tag}</span>`).join('')}</p>` : ''}
    </div>
  `).join('');
}

// 点击模态框外部关闭
document.addEventListener('click', function(e) {
  const modal = document.getElementById('projects-modal');
  if (modal && e.target === modal) {
    closeProjectsModal();
  }
});

// ESC 键关闭
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeProjectsModal();
  }
});

// 页面加载完成后
document.addEventListener('DOMContentLoaded', function() {
  renderProjects();

  // 修改"项目"链接行为
  const projectLinks = document.querySelectorAll('a[href="/categories/项目/"]');
  projectLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      openProjectsModal();
    });
  });
});
