const matrixCanvas = document.getElementById("matrix-canvas");
const typeScreen = document.getElementById("type-screen");

if (matrixCanvas) {
  const context = matrixCanvas.getContext("2d");
  const glyphs = "矩阵终端接入扫描追踪异常信道回显控制权限目标裂变1234567890";
  const fontSize = 18;
  let columns = 0;
  let drops = [];

  function resizeCanvas() {
    const scale = window.devicePixelRatio || 1;
    const width = window.innerWidth;
    const height = window.innerHeight;

    matrixCanvas.width = width * scale;
    matrixCanvas.height = height * scale;
    matrixCanvas.style.width = width + "px";
    matrixCanvas.style.height = height + "px";
    context.setTransform(scale, 0, 0, scale, 0, 0);

    columns = Math.ceil(width / fontSize);
    drops = Array.from({ length: columns }, () => Math.random() * -40);
  }

  function drawRain() {
    const width = window.innerWidth;
    const height = window.innerHeight;

    context.fillStyle = "rgba(1, 7, 3, 0.12)";
    context.fillRect(0, 0, width, height);
    context.font = `${fontSize}px monospace`;

    for (let i = 0; i < drops.length; i += 1) {
      const text = glyphs[Math.floor(Math.random() * glyphs.length)];
      const x = i * fontSize;
      const y = drops[i] * fontSize;
      const highlight = Math.random();

      context.fillStyle = highlight > 0.9 ? "#dcffe9" : highlight > 0.7 ? "#7effb3" : "#1dd763";
      context.fillText(text, x, y);

      if (y > height && Math.random() > 0.975) {
        drops[i] = Math.random() * -20;
      } else {
        drops[i] += 0.72 + highlight * 0.4;
      }
    }

    window.requestAnimationFrame(drawRain);
  }

  resizeCanvas();
  drawRain();
  window.addEventListener("resize", resizeCanvas);
}

if (typeScreen) {
  const lines = [
    "[终端] 正在建立加密会话",
    "[终端] 正在扫描可接入节点",
    "[节点一] 已截获异常链路定位请求",
    "[节点二] 正在比对时序波动与异常峰值",
    "[节点三] 已完成首轮权限校验",
    "[告警] 发现一处高频噪声区，已标记黄色",
    "[终端] 正在回吐摘要、告警与动作建议",
    "[完成] 全链路结果已写入当前会话"
  ];

  typeScreen.textContent = "";

  lines.forEach((line, index) => {
    window.setTimeout(() => {
      const row = document.createElement("p");
      row.className = "line";
      row.textContent = line;
      typeScreen.appendChild(row);
    }, 420 * index);
  });
}
