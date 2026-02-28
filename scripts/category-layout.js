// 禁用分类页面的默认布局
hexo.extend.filter.register('before_generate', function() {
  hexo.locals.get('pages').forEach(function(page) {
    if (page.layout === 'category') {
      page.layout = false;
    }
  });
});
