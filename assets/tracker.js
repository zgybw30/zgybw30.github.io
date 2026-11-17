/* zgybw30.github.io 访客统计埋点脚本
 *
 * 部署步骤（见 README）：
 *  1. 把下面的 WORKER_URL 换成真实的 Worker 地址，例如
 *     https://visitor-analytics.<你的子域名>.workers.dev
 *  2. 把本文件拷到品牌站仓库的 assets/tracker.js
 *  3. 在三个模板（home/harmony/todo_template.html）的 </body> 前加：
 *     <script src="/assets/tracker.js" defer></script>
 *     再跑 gen_site.py 重新生成 9 页并推送；works.html 直接加同一行。
 *
 * 隐私口径：只记匿名 UUID + 页面路径 + 来源，不记 IP、不记任何身份信息。
 * 排除本人：浏览器打开任意一页，地址栏后面加 ?optout=1 回车一次即可，
 * 本浏览器之后不再上报（localStorage 里写 hwa_optout=1）。
 */
(function () {
  'use strict';

  // TODO（部署后替换）：Worker 地址，不要带末尾斜杠
  var WORKER_URL = 'https://visitor-analytics.tanghsine.workers.dev';
  var ENDPOINT = WORKER_URL + '/collect';

  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    // 旧浏览器回退：Math.random 生成 v4 格式 UUID
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = (Math.random() * 16) | 0;
      return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
    });
  }

  try {
    var qs = window.location.search || '';

    // ?optout=1：本浏览器不再上报（排除本人用），本次也不统计
    if (qs.indexOf('optout=1') !== -1) {
      localStorage.setItem('hwa_optout', '1');
      return;
    }
    // ?optout=0：取消排除，恢复上报
    if (qs.indexOf('optout=0') !== -1) {
      localStorage.removeItem('hwa_optout');
    }
    if (localStorage.getItem('hwa_optout') === '1') return;

    var vid = localStorage.getItem('hwa_vid');
    if (!vid) {
      vid = uuid();
      try {
        localStorage.setItem('hwa_vid', vid);
      } catch (e) {
        // 隐私模式写不进 localStorage 也没关系：本次用临时 ID，
        // 服务端收不到合法 UUID 时会用当日哈希兜底
      }
    }

    var payload = JSON.stringify({
      v: vid,
      p: window.location.pathname || '/',
      r: document.referrer || '',
    });

    // sendBeacon 是页面卸载时也能发出去的首选；失败则 fetch keepalive 兜底。
    // 字符串 payload 默认走 text/plain，不触发 CORS 预检。
    if (navigator.sendBeacon) {
      if (navigator.sendBeacon(ENDPOINT, payload)) return;
    }
    fetch(ENDPOINT, {
      method: 'POST',
      body: payload,
      keepalive: true,
      headers: { 'Content-Type': 'text/plain' },
    }).catch(function () {});
  } catch (e) {
    // 统计永远不能影响页面本身，出错就静默放弃
  }
})();
