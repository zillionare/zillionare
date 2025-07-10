---
title: 量化好声音播客
---

<div class="podcast-grid">
  <div class="podcast-card">
    <div class="podcast-info">
      <h3><a href="/podcast/10-trading-agents/">多智能体交易框架：AI如何模拟真实交易团队决策？</a></h3>
      <p class="podcast-date">2025-07-10</p>
      <p class="podcast-desc">一个月内GitHub暴增7k星标的TradingAgents框架有何特别？本期节目揭秘这个由UC Berkeley和MIT学者开发的多智能体交易系统如何模拟真实交易团队协作。不同于传统金融大模型仅专注于NLP任务，TradingAgents通过结构化通讯协议让AI扮演分析师、研究员、交易员和风控等角色，实现『真理越辩越明』的决策机制。回测显示，该框架在Apple、Google等标的上年化收益提升30%，最大回撤仅2.11%。AI交易团队时代，人类金融专业人士将如何应对？</p>
      <audio controls><source src="https://cdn.jsdelivr.net/gh/zillionare/podcast@main/2025/07/10-final.mp3" type="audio/mpeg">您的浏览器不支持音频播放。</audio>
    </div>
  </div>
  <div class="podcast-card">
    <div class="podcast-info">
      <h3><a href="/podcast/13-ubl-2/">UBL因子：工具之困与意外发现</a></h3>
      <p class="podcast-date">2025-07-09</p>
      <p class="podcast-desc">Alphalens无法处理月度因子，Aaron开发Moonshot解决难题。UBL因子不仅复现成功，效果超预期。更令人惊讶的是，威廉下影线因子表现与直觉相反——下影线均值越小，后市反而越看涨，挑战了传统交易经验。</p>
      <audio controls><source src="https://cdn.jsdelivr.net/gh/zillionare/podcast@main/2025/07/13.mp3" type="audio/mpeg">您的浏览器不支持音频播放。</audio>
    </div>
  </div>
  <div class="podcast-card">
    <div class="podcast-info">
      <h3><a href="/podcast/12-量化交易是怎么控制风险的/">水晶球实现揭秘：为什么量化比主观交易更能控制风险？</a></h3>
      <p class="podcast-date">2025-07-08</p>
      <p class="podcast-desc">主观投资者即使拥有『水晶球』也会亏损，为何量化交易能更好地控制风险？本期节目揭示了维克托·哈加尼的惊人实验结果：一半受过训练的投资者亏损，六分之一直接爆仓。我们深入探讨量化交易如何通过科学决策、严谨回测和严格执行来降低风险，并分享三大验证策略有效性的方法：参数稳定性测试、系统性错误排查和策略仿真。告别『回测买地球，实盘亏成狗』的困境！</p>
      <audio controls><source src="https://cdn.jsdelivr.net/gh/zillionare/podcast@main/2025/07/12-final.mp3" type="audio/mpeg">您的浏览器不支持音频播放。</audio>
    </div>
  </div>
</div>

<style>
.podcast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.podcast-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: #fff;
}

.podcast-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.podcast-info {
  padding: 20px;
}

.podcast-info h3 {
  margin: 0 0 10px 0;
  font-size: 1.2em;
}

.podcast-info h3 a {
  text-decoration: none;
  color: #333;
}

.podcast-info h3 a:hover {
  color: #007acc;
}

.podcast-date {
  color: #666;
  font-size: 0.9em;
  margin: 5px 0;
}

.podcast-desc {
  font-size: 0.95em;
  color: #555;
  margin: 10px 0;
  line-height: 1.4;
}

.podcast-info audio {
  width: 100%;
  margin-top: 15px;
}
</style>
