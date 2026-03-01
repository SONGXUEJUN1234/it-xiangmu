(function($){
  // Search
  var $searchWrap = $('#search-form-wrap'),
    isSearchAnim = false,
    searchAnimDuration = 200;

  var startSearchAnim = function(){
    isSearchAnim = true;
  };

  var stopSearchAnim = function(callback){
    setTimeout(function(){
      isSearchAnim = false;
      callback && callback();
    }, searchAnimDuration);
  };

  $('.nav-search-btn').on('click', function(){
    if (isSearchAnim) return;

    startSearchAnim();
    $searchWrap.addClass('on');
    stopSearchAnim(function(){
      $('.search-form-input').focus();
    });
  });

  $('.search-form-input').on('blur', function(){
    startSearchAnim();
    $searchWrap.removeClass('on');
    stopSearchAnim();
  });

  // Share
  $('body').on('click', function(){
    $('.article-share-box.on').removeClass('on');
  }).on('click', '.article-share-link', function(e){
    e.stopPropagation();

    var $this = $(this),
      url = $this.attr('data-url'),
      encodedUrl = encodeURIComponent(url),
      id = 'article-share-box-' + $this.attr('data-id'),
      title = $this.attr('data-title'),
      offset = $this.offset();

    if ($('#' + id).length){
      var box = $('#' + id);

      if (box.hasClass('on')){
        box.removeClass('on');
        return;
      }
    } else {
      var html = [
        '<div id="' + id + '" class="article-share-box">',
          '<input class="article-share-input" value="' + url + '">',
          '<div class="article-share-links">',
            '<a href="https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodedUrl + '" class="article-share-twitter" target="_blank" title="Twitter"><span class="fa fa-twitter"></span></a>',
            '<a href="https://www.facebook.com/sharer.php?u=' + encodedUrl + '" class="article-share-facebook" target="_blank" title="Facebook"><span class="fa fa-facebook"></span></a>',
            '<a href="http://pinterest.com/pin/create/button/?url=' + encodedUrl + '" class="article-share-pinterest" target="_blank" title="Pinterest"><span class="fa fa-pinterest"></span></a>',
            '<a href="https://www.linkedin.com/shareArticle?mini=true&url=' + encodedUrl + '" class="article-share-linkedin" target="_blank" title="LinkedIn"><span class="fa fa-linkedin"></span></a>',
          '</div>',
        '</div>'
      ].join('');

      var box = $(html);

      $('body').append(box);
    }

    $('.article-share-box.on').hide();

    box.css({
      top: offset.top + 25,
      left: offset.left
    }).addClass('on');
  }).on('click', '.article-share-box', function(e){
    e.stopPropagation();
  }).on('click', '.article-share-box-input', function(){
    $(this).select();
  }).on('click', '.article-share-box-link', function(e){
    e.preventDefault();
    e.stopPropagation();

    window.open(this.href, 'article-share-box-window-' + Date.now(), 'width=500,height=450');
  });

  // Caption
  $('.article-entry').each(function(i){
    $(this).find('img').each(function(){
      if ($(this).parent().hasClass('fancybox') || $(this).parent().is('a')) return;

      var alt = this.alt;

      if (alt) $(this).after('<span class="caption">' + alt + '</span>');

      $(this).wrap('<a href="' + this.src + '" data-fancybox=\"gallery\" data-caption="' + alt + '"></a>')
    });

    $(this).find('.fancybox').each(function(){
      $(this).attr('rel', 'article' + i);
    });
  });

  if ($.fancybox){
    $('.fancybox').fancybox();
  }

  // Mobile nav
  var $container = $('#container'),
    isMobileNavAnim = false,
    mobileNavAnimDuration = 200;

  var startMobileNavAnim = function(){
    isMobileNavAnim = true;
  };

  var stopMobileNavAnim = function(){
    setTimeout(function(){
      isMobileNavAnim = false;
    }, mobileNavAnimDuration);
  }

  $('#main-nav-toggle').on('click', function(){
    if (isMobileNavAnim) return;

    startMobileNavAnim();
    $container.toggleClass('mobile-nav-on');
    stopMobileNavAnim();
  });

  $('#wrap').on('click', function(){
    if (isMobileNavAnim || !$container.hasClass('mobile-nav-on')) return;

    $container.removeClass('mobile-nav-on');
  });

  var matrixCanvas = document.getElementById('matrix-rain');

  if (matrixCanvas && matrixCanvas.getContext){
    var matrixContext = matrixCanvas.getContext('2d'),
      matrixChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789$+-*/=%"\'#&_(),.;:[]{}<>01',
      fontSize = 16,
      columns = 0,
      drops = [],
      animationFrameId = null,
      lastRender = 0,
      renderInterval = 66;

    var setupMatrix = function(){
      var scale = window.devicePixelRatio || 1,
        width = window.innerWidth,
        height = window.innerHeight;

      matrixCanvas.width = width * scale;
      matrixCanvas.height = height * scale;
      matrixCanvas.style.width = width + 'px';
      matrixCanvas.style.height = height + 'px';
      matrixContext.setTransform(scale, 0, 0, scale, 0, 0);
      columns = Math.ceil(width / fontSize);
      drops = [];

      for (var i = 0; i < columns; i++){
        drops.push(Math.random() * -60);
      }
    };

    var renderMatrix = function(timestamp){
      if (!lastRender || timestamp - lastRender >= renderInterval){
        var width = window.innerWidth,
          height = window.innerHeight;

        matrixContext.fillStyle = 'rgba(1, 8, 4, 0.16)';
        matrixContext.fillRect(0, 0, width, height);
        matrixContext.font = fontSize + 'px monospace';

        for (var i = 0; i < drops.length; i++){
          var text = matrixChars.charAt(Math.floor(Math.random() * matrixChars.length)),
            x = i * fontSize,
            y = drops[i] * fontSize,
            intensity = Math.random();

          matrixContext.fillStyle = intensity > 0.92 ? '#d6ffe6' : intensity > 0.7 ? '#79ffb0' : '#1ec75b';
          matrixContext.fillText(text, x, y);

          if (y > height && Math.random() > 0.975){
            drops[i] = Math.random() * -25;
          } else {
            drops[i] += 1 + intensity * 0.35;
          }
        }

        lastRender = timestamp;
      }

      animationFrameId = window.requestAnimationFrame(renderMatrix);
    };

    setupMatrix();
    animationFrameId = window.requestAnimationFrame(renderMatrix);

    window.addEventListener('resize', function(){
      window.cancelAnimationFrame(animationFrameId);
      lastRender = 0;
      setupMatrix();
      animationFrameId = window.requestAnimationFrame(renderMatrix);
    });
  }
})(jQuery);
