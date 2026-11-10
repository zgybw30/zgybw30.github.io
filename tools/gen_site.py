# -*- coding: utf-8 -*-
"""Generate index.html / en.html / ja.html from tools/site_template.html.
Standard product-page design: product-first, minimal personal content.
Run from anywhere: python3 tools/gen_site.py  (writes to the repo root)."""
import io, os, re

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
TPL = io.open(os.path.join(_HERE, 'site_template.html'), encoding='utf-8').read()

def feats_html(feats):
    return '\n'.join('          <li>%s</li>' % f for f in feats)

def steps_html(steps):
    return '\n'.join(
        '      <div class="step reveal"><div class="num">%d</div><h3>%s</h3><p>%s</p></div>' % (i, h, p)
        for i, (h, p) in enumerate(steps, 1))

def chips_html(chips):
    return ''.join('<span class="paychip">%s</span>' % c for c in chips)

def faq_html(items):
    return '\n'.join(
        '    <details class="faq reveal">\n      <summary>%s</summary>\n      <p>%s</p>\n    </details>' % (q, a)
        for q, a in items)

ZH = dict(
    LANG="zh-CN",
    TITLE="Harmony · 本地 AI 视觉生产工作台",
    META="Harmony：为短视频创作者打造的桌面工作台——图像编辑、图层、本地 AI 生图与 AI 视频。14 天全功能免费试用，一次性买断。",
    NAV_FEATURES="功能", NAV_SHOWCASE="展示", NAV_PRICING="价格", NAV_BUY="购买",
    HERO_BADGE="本地优先 · 一次买断 · 14 天免费试用",
    HERO_H1='Harmony<br>本地 AI 视觉生产工作台',
    HERO_LEAD="为短视频创作者打造的桌面工作台：图像编辑、图层、本地 AI 生图与 AI 视频，全在你自己的电脑上完成。素材不出本机，不排队，不按量付费。",
    HERO_CTA1="¥129 购买专业版", HERO_CTA2="了解功能",
    ST1B="14 天", ST1S="全功能免费试用", ST2B="一次性", ST2S="买断 · 无订阅",
    ST3B="2.x", ST3S="版本内免费更新", ST4B="100%", ST4S="本地运行",
    SHOT0="软件界面展示图（待生成）",
    F_KICKER="功能", F_H2="一个工作台，从修图到出片",
    F_DESC="把分散的工具收拢到一条生产线上：编辑、生图、生视频、组装，都在本地完成。",
    FEAT1T="图像编辑与图层", FEAT1P="裁剪、调色、蒙版、调整层与图层样式，日常修图一站完成。",
    FEAT2T="本地 AI 生图", FEAT2P="Qwen-Image 2.1 在本机运行，文生图与图生图，不上传、不排队。",
    FEAT3T="AI 视频与制片画布", FEAT3P="MiniMax-H3 本地生成视频，分镜、参考图、组装成片一条线走完。",
    FEAT4T="剧本助手", FEAT4P="写作模型帮你润色剧本、拆解分镜，把想法变成可执行的工作流。",
    FEAT5T="模板与内容包", FEAT5P="工作流模板与内容包导入，跑通的流程存下来，一键复用。",
    FEAT6T="本地优先 · 离线授权", FEAT6P="素材与模型都在本机，离线签名授权，不注册账号、不联网验证。",
    SH_KICKER="展示", SH_H2="Harmony 长这样",
    SH_DESC="界面展示用软件真实截图；风格样张由 Harmony 的 AI 生图生成。",
    SHOT1="风格样张 1 · 赛博朋克", SHOT2="风格样张 2 · 水墨山水",
    SHOT3="风格样张 3 · 极简几何", SHOT4="风格样张 4 · 电影感写实",
    B_KICKER="价格", B_H2="简单定价，买断制",
    B_DESC="先免费试用 14 天，全功能开放；觉得好用，再一次性买断。",
    PRICE_BADGE="首发价", PRICE_NAME="Harmony 专业版",
    PRICE_NOTE="一次性买断 · 无订阅",
    PRICE_FEATS=["全部生成与编辑功能解锁", "导出无水印", "2.x 版本内免费更新",
                 "离线激活，不注册账号", "授权绑定一台电脑，换机免费换绑", "达不到最低配置，全额退款"],
    BUY_BTN="立即购买 ¥129 →",
    PAY_CHIPS=["微信支付", "支付宝", "授权文件邮箱交付", "24 小时内发码", "离线激活"],
    BUY_NOTE="付款走爱发电（支持微信 / 支付宝）。店铺正在上架中：上架前点上方按钮会跳到页脚联系区，联系我转账购买即可——价格不变，同样 24 小时内发授权文件。",
    CFG_H3="配置要求",
    CFG_P1="本地 AI 生成吃显卡：<strong style=\"color:var(--ink)\">最低 RTX 3060 12GB 起步，推荐 RTX 3090 级别</strong>，内存建议 16GB 以上。达不到最低配置请先别买；已购买发现达不到的，全额退款。",
    CFG_P2="模型文件需自备（软件不内置权重），可在魔搭社区免费下载，FAQ 里有说明。",
    STEPS_H3="购买只要三步",
    STEPS=[("免费试用 14 天", "下载 Windows 安装包（入口上线中，先通过页脚联系方式获取试用包），全功能开放 14 天。"),
           ("爱发电付款", "在爱发电下单，支持微信 / 支付宝；下单时把邮箱和软件「系统 → 授权管理」里显示的本机机器码一起发我，授权绑定你的这台电脑，文件发到你的邮箱。"),
           ("导入即激活", "24 小时内收到授权文件，在 Harmony「系统 → 授权管理」里导入，立即生效。")],
    STEPS_NOTE="离线激活全程不需要联网；试用期间的作品与设置在激活后完整保留。",
    FAQ_H2="购买前常见问题",
    FAQS=[("我的电脑能跑吗？",
           "本地图像与视频生成主要吃显卡显存。最低 RTX 3060 12GB（视频功能按低显存方式使用），推荐 RTX 3090 级别，内存建议 16GB 以上。达不到最低配置的请先不要购买；已购买后确认达不到的，全额退款。"),
          ("模型文件从哪里下载？",
           "软件不内置任何模型权重，需要自备：Qwen-Image-2.1（图像）与 MiniMax-H3（视频）的 GGUF 权重都可以在魔搭社区（ModelScope）免费下载，在软件「设置」里逐个选到对应文件即可。权重许可归各自模型方所有，请按其许可使用。"),
          ("试用版和专业版有什么区别？",
           "下载后先有 14 天全功能试用。试用到期进入免费版：生成停用、导出带水印。购买并导入授权文件后立即恢复全部功能，导出无水印。"),
          ("激活需要联网或注册账号吗？",
           "不需要。授权是离线签名文件：购买后你会收到一个授权文件，在软件里导入即完成激活，不注册、不绑账号、不回连服务器验证。"),
          ("第一次运行被 Windows 拦截怎么办？",
           "软件目前还没有做数字签名，Windows SmartScreen 可能弹出蓝色提示。点「更多信息」→「仍要运行」即可。请只从本站或官方渠道下载，不要用第三方来源的安装包。"),
          ("授权能用在几台电脑上？",
           "一份授权绑定一台电脑：下单时把软件「授权管理」里显示的机器码连同邮箱一起发我即可。换电脑或重装系统联系我免费换绑（提供新机器码），旧的那份同时吊销。"),
          ("可以退款吗？",
           "电脑达不到最低配置的，全额退款。其他情况通过爱发电订单或页脚联系方式找我处理。")],
    FOOT_BINANCE="币安广场 @zgybw",
    FOOT_PRODUCTS="产品站",
    FOOT_NOTE="这里是 hsine 的产品站，Harmony 是目前在售的产品，后续会有更多产品加入。购买、反馈与合作请通过上方联系方式。",
)

EN = dict(
    LANG="en",
    TITLE="Harmony · Local AI Visual Production Studio",
    META="Harmony: a desktop studio for short-video creators — image editing, layers, local AI image and video generation. 14-day full trial, one-time purchase.",
    NAV_FEATURES="Features", NAV_SHOWCASE="Showcase", NAV_PRICING="Pricing", NAV_BUY="Buy",
    HERO_BADGE="Local-first · One-time purchase · 14-day free trial",
    HERO_H1='Harmony<br>The Local AI Visual Studio',
    HERO_LEAD="A desktop studio for short-video creators: image editing, layers, local AI image and video generation — all on your own computer. Your media never leaves your machine. No queues, no per-use fees.",
    HERO_CTA1="Buy Pro — ¥129", HERO_CTA2="Explore features",
    ST1B="14 days", ST1S="Full-featured free trial", ST2B="One-time", ST2S="No subscription",
    ST3B="2.x", ST3S="Free updates included", ST4B="100%", ST4S="Runs locally",
    SHOT0="App UI showcase (to be generated)",
    F_KICKER="Features", F_H2="One studio, from edit to final cut",
    F_DESC="The whole pipeline on one desk, running locally: edit, generate images, generate video, assemble.",
    FEAT1T="Image editing & layers", FEAT1P="Crop, color, masks, adjustment layers and layer styles — everyday editing in one place.",
    FEAT2T="Local AI image generation", FEAT2P="Qwen-Image 2.1 runs on your machine: text-to-image and image editing, no uploads, no queues.",
    FEAT3T="AI video & production canvas", FEAT3P="Local MiniMax-H3 video generation; storyboards, references and assembly in one flow.",
    FEAT4T="Script assistant", FEAT4P="A writing model that polishes scripts and breaks them into storyboards and executable workflows.",
    FEAT5T="Templates & content packs", FEAT5P="Import workflow templates and content packs; save what works and reuse it in one click.",
    FEAT6T="Local-first, offline licensing", FEAT6P="Media and models stay on your PC. Signed offline license — no account, no phone-home.",
    SH_KICKER="Showcase", SH_H2="What Harmony looks like",
    SH_DESC="Real UI screenshots; style samples generated with Harmony's own AI engine.",
    SHOT1="Style sample 1 · Cyberpunk", SHOT2="Style sample 2 · Ink landscape",
    SHOT3="Style sample 3 · Minimal geometry", SHOT4="Style sample 4 · Cinematic realism",
    B_KICKER="Pricing", B_H2="Simple pricing, buy once",
    B_DESC="Start with a 14-day free trial with every feature open. Buy once only if it earns its place.",
    PRICE_BADGE="LAUNCH OFFER", PRICE_NAME="Harmony Pro",
    PRICE_NOTE="One-time purchase (≈ US$18, list ¥199 ≈ US$28)",
    PRICE_FEATS=["All generation and editing features unlocked", "No watermarks on exports",
                 "Free updates within the 2.x line", "Offline activation — no account",
                 "Licensed to one computer; free rebind when you change machines",
                 "Full refund if your PC is below the minimum spec"],
    BUY_BTN="Buy now — ¥129 →",
    PAY_CHIPS=["License delivered by email", "Within 24 hours", "Offline activation", "No account needed"],
    BUY_NOTE="International checkout (Lemon Squeezy / Paddle) is in preparation. Until it opens, the button above takes you to the contact links in the footer — buy directly from me at the same price, with the same 24-hour license delivery.",
    CFG_H3="System requirements",
    CFG_P1="Local AI generation is GPU-hungry: <strong style=\"color:var(--ink)\">minimum RTX 3060 12GB, RTX 3090-class recommended</strong>, 16GB RAM or more suggested. Below the minimum, please don't buy — and if you bought and turn out to be below it, you get a full refund.",
    CFG_P2="Model weights are not bundled with the app; they are free to download (see the FAQ).",
    STEPS_H3="Buying takes three steps",
    STEPS=[("Start the free trial", "Download the Windows installer (public download going live — until then, get the trial package via the contact links below). Every feature is open for 14 days."),
           ("Purchase", "International checkout is being set up; for now, contact me below with your email and the machine code shown in the app under System → License — your license is bound to that computer and the file is sent to your email."),
           ("Import and you're activated", "Your license file arrives within 24 hours. Import it in Harmony under System → License and you're done.")],
    STEPS_NOTE="Activation is fully offline. Your trial-period work and settings carry over untouched.",
    FAQ_H2="Questions before you buy",
    FAQS=[("Can my PC run it?",
           "Local image and video generation lean on your GPU's VRAM. Minimum RTX 3060 12GB (video uses the low-VRAM configuration there), RTX 3090-class recommended, 16GB RAM or more suggested. If your machine is below the minimum, please don't buy; if you already bought and are below it, you get a full refund."),
          ("Where do I get the model weights?",
           "The app bundles no model weights — you supply your own. The GGUF weights for Qwen-Image-2.1 (images) and MiniMax-H3 (video) are free to download from ModelScope, and the app's Settings point at each file. Each model's license stays with its provider; please follow those terms."),
          ("Trial vs. Pro — what's the difference?",
           "You get 14 days with every feature. When the trial ends, the free version disables generation and exports carry a watermark. Importing a license restores everything immediately, watermark-free."),
          ("Does activation need internet or an account?",
           "No. Your license is an offline signed file: import it in the app and activation is complete. No registration, no machine account, no server check-in."),
          ("Windows SmartScreen is blocking the app — what now?",
           "The app is not code-signed yet, so SmartScreen may show a blue warning. Click “More info” → “Run anyway”. Only download from this site or official channels, never from third-party mirrors."),
          ("How many computers can I use it on?",
           "One license binds to one computer: when you order, send me your email and the machine code shown in the app (System → License). If you replace your PC or reinstall Windows, contact me for a free rebind with the new machine code — the old license is revoked at the same time."),
          ("What about refunds?",
           "Full refund if your PC is below the minimum requirements. For anything else, reach me through your order or the contact links and we'll sort it out."),
          ("Any regional limits I should know about?",
           "The app itself is sold worldwide. One caveat: the local video features use MiniMax-H3 weights, whose community license does not permit local deployment in the US, EU, UK or South Korea. Image features are unaffected everywhere.")],
    FOOT_BINANCE="Binance Square @zgybw",
    FOOT_PRODUCTS="PRODUCTS",
    FOOT_NOTE="This is hsine's product site. Harmony is the product currently on sale; more products will follow. Purchases, feedback and collaborations: use the contact links above.",
)

JA = dict(
    LANG="ja",
    TITLE="Harmony · ローカル AI 映像制作スタジオ",
    META="Harmony：短編動画クリエイター向けデスクトップスタジオ。画像編集、レイヤー、ローカル AI 画像・動画生成。14日間全機能無料トライアル、買い切り。",
    NAV_FEATURES="機能", NAV_SHOWCASE="ショーケース", NAV_PRICING="価格", NAV_BUY="購入",
    HERO_BADGE="ローカル優先 · 買い切り · 14日間無料トライアル",
    HERO_H1='Harmony<br>ローカル AI 映像制作スタジオ',
    HERO_LEAD="短編動画クリエイターのためのデスクトップスタジオ：画像編集、レイヤー、ローカル AI 画像生成と AI 動画生成を、すべて自分の PC の中で。素材は外に出ず、待ち行列も従量課金もありません。",
    HERO_CTA1="Pro を購入 — ¥129", HERO_CTA2="機能を見る",
    ST1B="14日間", ST1S="全機能無料トライアル", ST2B="買い切り", ST2S="サブスクなし",
    ST3B="2.x", ST3S="無料アップデート込み", ST4B="100%", ST4S="ローカル実行",
    SHOT0="アプリ UI ショーケース（生成予定）",
    F_KICKER="機能", F_H2="修整から完成まで、一つのスタジオで",
    F_DESC="編集、画像生成、動画生成、組み立てまで。制作の流れをすべてローカルで完結させます。",
    FEAT1T="画像編集とレイヤー", FEAT1P="切り抜き、色調整、マスク、調整レイヤーとレイヤースタイル。日常の編集はここで完結。",
    FEAT2T="ローカル AI 画像生成", FEAT2P="Qwen-Image 2.1 を自分の PC で実行。テキストから画像も、画像の編集も。アップロードも待ち行列もなし。",
    FEAT3T="AI 動画と制作カンバス", FEAT3P="MiniMax-H3 のローカル動画生成。絵コンテ、参考画像、組み立てまで一つの流れで。",
    FEAT4T="シナリオアシスタント", FEAT4P="ライティングモデルが脚本を推敲し、絵コンテと実行可能なワークフローに分解します。",
    FEAT5T="テンプレートとコンテンツパック", FEAT5P="ワークフローテンプレートとパックをインポート。うまくいった流れを保存して再利用。",
    FEAT6T="ローカル優先 · オフライン認証", FEAT6P="素材もモデルも PC の中。署名付きオフラインライセンスで、アカウント登録もサーバー確認も不要。",
    SH_KICKER="ショーケース", SH_H2="Harmony の画面",
    SH_DESC="実際の UI スクリーンショットと、Harmony 自身の AI で生成した作例を掲載予定です。",
    SHOT1="作例 1 · サイバーパンク", SHOT2="作例 2 · 水墨山水",
    SHOT3="作例 3 · ミニマルジオメトリ", SHOT4="作例 4 · シネマティック写実",
    B_KICKER="価格", B_H2="シンプルな買い切り価格",
    B_DESC="まずは 14日間、全機能を無料でお試しください。納得できたら買い切りでどうぞ。",
    PRICE_BADGE="発売記念", PRICE_NAME="Harmony Pro",
    PRICE_NOTE="買い切り（中国価格 ¥129／約 US$18、定価 ¥199）",
    PRICE_FEATS=["全生成・編集機能を解放", "書き出しにウォーターマークなし",
                 "2.x の間は無料アップデート", "オフライン認証、アカウント不要",
                 "ライセンスは PC 1台に紐付け、買い替え時は無料で付け替え",
                 "最低要件を満たさない場合は全額返金"],
    BUY_BTN="今すぐ購入 — ¥129 →",
    PAY_CHIPS=["ライセンスはメール交付", "24時間以内", "オフライン認証", "アカウント不要"],
    BUY_NOTE="海外向け決済（Lemon Squeezy / Paddle）は準備中です。それまでは上のボタンを押すとフッターの連絡先に移動します。直接のご購入でも価格は同じで、24時間以内にライセンスファイルを送ります。",
    CFG_H3="動作環境",
    CFG_P1="ローカル AI 生成は GPU を使います：<strong style=\"color:var(--ink)\">最低 RTX 3060 12GB、推奨 RTX 3090 クラス</strong>、メモリは 16GB 以上推奨。最低要件を満たさない場合は購入をお控えください。購入後に満たないことが判明した場合は全額返金します。",
    CFG_P2="モデル本体はアプリに含まれません。無料でダウンロードできます（FAQ 参照）。",
    STEPS_H3="購入は 3 ステップ",
    STEPS=[("14日間無料トライアル", "Windows インストーラーをダウンロード（公開ダウンロードは準備中。それまでは下の連絡先から試用パッケージをお渡しします）。全機能が 14日間使えます。"),
           ("購入の申込", "海外向け決済は準備中のため、当面は下の連絡先からお申し込みください。メールアドレスと、アプリの「システム → ライセンス管理」に表示されるマシン コードをお知らせください。ライセンスはその PC に紐付き、ファイルはメールで送ります。"),
           ("インポートで即時有効化", "24時間以内に届くライセンスファイルを、Harmony の「システム → ライセンス管理」からインポートすれば完了です。")],
    STEPS_NOTE="認証は完全オフライン。トライアル中の作品と設定はそのまま引き継がれます。",
    FAQ_H2="購入前のよくある質問",
    FAQS=[("私の PC で動きますか？",
           "ローカルでの画像・動画生成は GPU の VRAM を使います。最低 RTX 3060 12GB（動画は低 VRAM 向け設定で使用）、推奨 RTX 3090 クラス、メモリ 16GB 以上推奨。最低要件を満たさない場合は購入をお控えください。購入後に満たないことが判明した場合は全額返金します。"),
          ("モデルファイルはどこで入手しますか？",
           "アプリにモデル本体は含まれません。Qwen-Image-2.1（画像）と MiniMax-H3（動画）の GGUF ウェイトは ModelScope で無料ダウンロードでき、アプリの「設定」から各ファイルを指定します。各モデルのライセンスは提供元の条件に従ってください。"),
          ("トライアルと Pro の違いは？",
           "14日間は全機能が使えます。期限が過ぎると無料版になり、生成が停止し、書き出しにウォーターマークが入ります。ライセンスファイルをインポートすれば即座に全機能が戻り、ウォーターマークも消えます。"),
          ("認証にネット接続やアカウントは必要ですか？",
           "不要です。ライセンスはオフライン署名ファイルで、アプリにインポートするだけで認証完了。登録もサーバー確認もありません。"),
          ("Windows にブロックされます。どうすれば？",
           "現在まだコード署名がないため、SmartScreen の青い警告が出ることがあります。「詳細情報」→「実行」を選んでください。ダウンロードは必ず本サイトなど公式チャネルから行ってください。"),
          ("何台の PC で使えますか？",
           "ライセンスは PC 1台に紐付きます。注文時にメールアドレスと、アプリの「システム → ライセンス管理」に表示されるマシン コードをお知らせください。PC の買い替えや Windows の再インストール時は、新しいマシン コードで無料で付け替えます（旧ライセンスは同時に失効します）。"),
          ("返金はできますか？",
           "PC が最低要件を満たさない場合は全額返金します。その他の場合も、注文経由または連絡先からご相談ください。"),
          ("地域による制限はありますか？",
           "アプリ自体は全世界で販売しています。ただし動画機能で使う MiniMax-H3 ウェイトのコミュニティライセンスでは、米国・EU・英国・韓国でのローカル展開が制限されています（日本は対象外です）。画像機能はすべての地域で問題なく使えます。")],
    FOOT_BINANCE="Binance Square @zgybw",
    FOOT_PRODUCTS="製品",
    FOOT_NOTE="ここは hsine の製品サイトです。Harmony は現在販売中の製品で、今後さらに製品が加わります。購入・フィードバック・コラボのご相談は上の連絡先からどうぞ。",
)


def afeats_html(feats):
    return '\n'.join('          <li>%s</li>' % f for f in feats)

def info_html(rows):
    return '\n'.join(
        '        <div class="irow"><span>%s</span><b>%s</b></div>' % (k, v)
        for k, v in rows)

def timeline_html(items):
    return '\n'.join(
        '      <div class="tl-item reveal"><span class="tl-date">%s</span><h3>%s</h3><p>%s</p></div>' % (d, h, t)
        for d, h, t in items)


EXTRA = {
'index.html': dict(
    TOPBAR_TXT="本地 AI 视觉生产工作台 · 数据不出本机",
    TOPBAR_RIGHT="Harmony v2.0 已发布",
    NAV_ABOUT="关于",
    A_KICKER="ABOUT", A_H2="关于 Harmony",
    A_P1="Harmony 是由独立开发者 hsine 打造的本地 AI 视觉生产工作台：把图像编辑、图层、本地 AI 生图与批量流水线收拢到一个桌面软件里，为照相馆、工作室与短视频创作者的生产场景而做。",
    A_P2="它坚持本地运行的路线：模型与素材都在你自己的电脑上，断网可用；生成全程不经过任何第三方服务器，客户照片不出店、不出本机。",
    A_FEATS=["100% 本地运行，断网可用", "素材与作品不上传，数据不出本机",
             "离线签名授权，不注册账号、不联网验证", "一次买断，2.x 版本内免费更新"],
    INFO_TITLE="产品信息",
    INFO=[("产品名称", "Harmony"), ("产品类型", "桌面 AI 视觉生产软件"),
          ("运行平台", "Windows"), ("当前版本", "v2.0"),
          ("授权方式", "离线签名 · 绑定一台电脑"), ("开发者", "hsine（独立开发）")],
    V_KICKER="PRINCIPLES", V_H2="我们的坚持",
    V_DESC="做给生产场景用的工具，靠的是把几件简单的事一直做对。",
    VAL1T="本地优先", VAL1P="全部生成在本机完成，不依赖云端服务，断网照样开工。",
    VAL2T="数据不出本机", VAL2P="素材、模型与作品都在你的电脑上，不上传任何服务器。",
    VAL3T="一次买断", VAL3P="没有订阅，没有按量计费；买了就是你的，一直能用。",
    VAL4T="离线授权", VAL4P="签名授权文件离线激活，不注册、不绑账号、不回连验证。",
    VAL5T="持续更新", VAL5P="2.x 版本内免费更新，软件内检查更新、一键升级。",
    VAL6T="独立开发", VAL6P="由独立开发者制作与维护，反馈直达本人，不绕客服工单。",
    T_KICKER="HISTORY", T_H2="产品历程",
    T_DESC="从定名到正式发布，Harmony 的每一步都落在真实的生产需求上。",
    TL=[("2026.10", "产品定名 Harmony", "确定本地优先的产品路线与商业化方案：一次性买断、离线签名授权、绑定一台电脑。"),
        ("2026.11", "批量流水线上线", "面向照相馆与工作室的批量处理流水线：文件夹进、成品出，失败跳过、断点续跑。"),
        ("2026.11", "手机遥控上线", "手机扫码连接电脑，在局域网内遥控生成；数据不出店，遥控本身就是卖点。"),
        ("2026.11", "Harmony 2.0 正式发布", "首个正式版本发布，软件内自动更新链路打通：检查更新、下载、安装一气呵成。")],
    CTA_H="先免费试用 14 天，再决定买不买", CTA_P="全功能开放试用，试用期间的作品与设置在激活后完整保留。",
    CTA_BTN="¥129 购买专业版",
    F_ABOUT_P="本地 AI 视觉生产工具，全部在你自己的电脑上运行。由 hsine 独立制作与维护。",
    F_COL_P="产品", F_COL_R="资源", F_COL_C="联系",
    F_RES1="示例包下载", F_RES2="版本发布",
    F_WECHAT="微信 · zgybw（扫码添加）",
),
'en.html': dict(
    TOPBAR_TXT="Local AI visual production studio · Your data stays on your PC",
    TOPBAR_RIGHT="Harmony v2.0 released",
    NAV_ABOUT="About",
    A_KICKER="ABOUT", A_H2="About Harmony",
    A_P1="Harmony is a local AI visual production studio built by independent developer hsine. It brings image editing, layers, local AI image generation and batch pipelines into one desktop app, made for photo studios, workshops and short-video creators.",
    A_P2="It runs the local route on purpose: models and media live on your own computer and it works fully offline. Nothing passes through a third-party server — client photos never leave your shop or your machine.",
    A_FEATS=["100% local — works fully offline", "Media and work never upload; data stays on your PC",
             "Offline signed license — no account, no phone-home", "One-time purchase, free updates within 2.x"],
    INFO_TITLE="Product info",
    INFO=[("Product", "Harmony"), ("Type", "Desktop AI visual production app"),
          ("Platform", "Windows"), ("Current version", "v2.0"),
          ("Licensing", "Offline signed file · one computer"), ("Developer", "hsine (independent)")],
    V_KICKER="PRINCIPLES", V_H2="What we stand by",
    V_DESC="A tool for production work earns its place by getting a few simple things right, every time.",
    VAL1T="Local first", VAL1P="Every generation runs on your machine. No cloud dependency — it works offline.",
    VAL2T="Data stays put", VAL2P="Media, models and finished work live on your computer and upload nowhere.",
    VAL3T="Buy once", VAL3P="No subscription, no per-use fees. You buy it, you own it, it keeps working.",
    VAL4T="Offline licensing", VAL4P="A signed license file activates offline — no account, no server check-in.",
    VAL5T="Kept current", VAL5P="Free updates within the 2.x line, with in-app update checks and one-click upgrades.",
    VAL6T="Independent", VAL6P="Made and maintained by an independent developer — feedback reaches the person who builds it.",
    T_KICKER="HISTORY", T_H2="Product history",
    T_DESC="From naming to release, every step of Harmony answers a real production need.",
    TL=[("2026.10", "Named Harmony", "The local-first product route and commercial plan were set: one-time purchase, offline signed licensing, one computer per license."),
        ("2026.11", "Batch pipeline shipped", "Folder-in, finished-out batch processing for photo studios and workshops — failures skip, interrupted jobs resume."),
        ("2026.11", "Phone remote shipped", "Scan to connect and drive generation from your phone over the LAN. Data never leaves the shop — the remote is a feature, not a relay."),
        ("2026.11", "Harmony 2.0 released", "First formal release, with the in-app auto-update chain complete: check, download and install in one flow.")],
    CTA_H="Try everything free for 14 days", CTA_P="Every feature is open during the trial, and your work and settings carry over when you activate.",
    CTA_BTN="Buy Pro — ¥129",
    F_ABOUT_P="Local AI visual production tools that run entirely on your own machine. Built and maintained by hsine.",
    F_COL_P="Product", F_COL_R="Resources", F_COL_C="Contact",
    F_RES1="Sample pack download", F_RES2="Releases",
    F_WECHAT="WeChat — scan to add",
),
'ja.html': dict(
    TOPBAR_TXT="ローカル AI 映像制作スタジオ · データは PC の外に出ません",
    TOPBAR_RIGHT="Harmony v2.0 リリース",
    NAV_ABOUT="概要",
    A_KICKER="ABOUT", A_H2="Harmony について",
    A_P1="Harmony は独立開発者 hsine が作るローカル AI 映像制作スタジオです。画像編集、レイヤー、ローカル AI 画像生成、バッチパイプラインを一つのデスクトップアプリに集約し、写真館・工房・短編動画クリエイターの制作現場のために設計しました。",
    A_P2="ローカル実行にこだわります。モデルも素材も自分の PC の中にあり、オフラインで動作します。生成が第三者のサーバーを経由することはなく、お客様の写真が店の外に出ることもありません。",
    A_FEATS=["100% ローカル実行、オフラインで利用可能", "素材と作品はアップロードされず、データは PC 内に留まります",
             "オフライン署名ライセンス、アカウント登録・サーバー確認なし", "買い切り、2.x の間は無料アップデート"],
    INFO_TITLE="製品情報",
    INFO=[("製品名", "Harmony"), ("種別", "デスクトップ AI 映像制作ソフト"),
          ("対応 OS", "Windows"), ("現在のバージョン", "v2.0"),
          ("認証方式", "オフライン署名 · PC 1台に紐付け"), ("開発者", "hsine（独立開発）")],
    V_KICKER="PRINCIPLES", V_H2="私たちのこだわり",
    V_DESC="制作現場の道具は、いくつかのシンプルな約束を守り続けることで信頼を得ます。",
    VAL1T="ローカル優先", VAL1P="すべての生成は自分の PC で完結。クラウドに依存せず、オフラインでも働きます。",
    VAL2T="データは外に出ない", VAL2P="素材・モデル・完成品はすべてあなたの PC の中。どこにもアップロードしません。",
    VAL3T="買い切り", VAL3P="サブスクも従量課金もありません。買えばずっと使えます。",
    VAL4T="オフライン認証", VAL4P="署名付きライセンスファイルでオフライン認証。登録もサーバー確認も不要です。",
    VAL5T="継続アップデート", VAL5P="2.x の間は無料アップデート。アプリ内の確認からワンクリックで更新できます。",
    VAL6T="独立開発", VAL6P="独立開発者が制作・保守します。フィードバックは本人に直接届きます。",
    T_KICKER="HISTORY", T_H2="製品の歩み",
    T_DESC="命名から正式リリースまで、Harmony の一歩一歩は実際の制作ニーズに応えたものです。",
    TL=[("2026.10", "Harmony と命名", "ローカル優先の製品方針と商用プランを確定：買い切り、オフライン署名ライセンス、PC 1台への紐付け。"),
        ("2026.11", "バッチパイプライン公開", "写真館・工房向けのバッチ処理：フォルダを入れて完成品を出す。失敗はスキップ、中断したジョブは再開できます。"),
        ("2026.11", "スマホリモコン公開", "QR コードで PC に接続し、LAN 内でスマホから生成を操作。データは店の外に出ません。"),
        ("2026.11", "Harmony 2.0 正式リリース", "初の正式版を公開。アプリ内自動アップデート（確認・ダウンロード・インストール）まで一貫して動作します。")],
    CTA_H="まずは 14日間、無料で全機能をお試しください", CTA_P="トライアル中の作品と設定は、アクティベーション後もそのまま引き継がれます。",
    CTA_BTN="Pro を購入 — ¥129",
    F_ABOUT_P="ローカル AI 映像制作ツール。すべて自分の PC で動作します。hsine が独立して制作・保守しています。",
    F_COL_P="製品", F_COL_R="リソース", F_COL_C="連絡先",
    F_RES1="サンプルパック", F_RES2="リリース",
    F_WECHAT="WeChat — スキャンして追加",
),
}

for name, t in (('index.html', ZH), ('en.html', EN), ('ja.html', JA)):
    subs = dict(t)
    subs.update(EXTRA[name])
    subs['A_FEATS'] = afeats_html(EXTRA[name]['A_FEATS'])
    subs['INFO_ROWS'] = info_html(EXTRA[name]['INFO'])
    subs['TIMELINE'] = timeline_html(EXTRA[name]['TL'])
    subs['PRICE_FEATS'] = feats_html(t['PRICE_FEATS'])
    subs['STEPS'] = steps_html(t['STEPS'])
    subs['FAQS'] = faq_html(t['FAQS'])
    subs['PAY_CHIPS'] = chips_html(t['PAY_CHIPS'])
    subs['LSEL_ZH'] = 'on' if name == 'index.html' else ''
    subs['LSEL_EN'] = 'on' if name == 'en.html' else ''
    subs['LSEL_JA'] = 'on' if name == 'ja.html' else ''
    html = TPL
    for k, v in subs.items():
        if isinstance(v, str):
            html = html.replace('@' + k + '@', v)
    leftover = re.findall(r'@[A-Z0-9_]+@', html)
    assert not leftover, (name, leftover)
    assert 'cobalt' not in html and '个人产品' not in html
    io.open(os.path.join(_ROOT, name), 'w', encoding='utf-8').write(html)
    print('wrote', name, len(html))
print('OK')
