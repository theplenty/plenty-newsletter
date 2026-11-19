"""Build the PLENTY CONVENTION e-mail newsletter.

Run from the project root:  python -I tools/build_html.py 2026-11
Writes  <issue>/index.html     (absolute image URLs, the file that is sent)
        <issue>/_preview.html  (relative image URLs, for local checking)
"""
import io
import os
import sys

ISSUE = sys.argv[1] if len(sys.argv) > 1 else "2026-11"
BASE = "https://theplenty.github.io/plenty-newsletter/%s/" % ISSUE

# ── typography ────────────────────────────────────────────────────────────
EN = "'Cormorant','Cormorant Garamond',Georgia,'Times New Roman',serif"
KO = "'Nanum Myeongjo','NanumMyeongjo','나눔명조','Batang','바탕',Georgia,serif"

# ── palette ───────────────────────────────────────────────────────────────
G = "#0e3b2c"       # key colour: deep green
G_DEEP = "#0a2c21"  # footer
G_LINE = "#2a5846"  # hairline on green
IVORY = "#f7f3ea"   # page
PAPER = "#fdfbf6"   # cards
LINE = "#ddd3bd"    # hairline on ivory
GOLD = "#a5834a"    # accent on light
GOLD_L = "#cfb47c"  # accent on green
INK = "#1c2a24"
MUTE = "#69746c"
ON_G = "#f4eee0"    # text on green
ON_G_SOFT = "#b9c6bc"

# ── links (from the brief) ────────────────────────────────────────────────
L_HOME = "https://theplenty.co.kr/"
L_SCHEDULE = "https://theplenty.co.kr/schedule/"
L_BLOG = "https://blog.naver.com/plentyconvention"
_POST = "https://blog.naver.com/PostView.naver?blogId=plentyconvention&amp;logNo=%s&amp;categoryNo=%s&amp;parentCategoryNo=&amp;from=thumbnailList"
L_SPACE = _POST % ("224260162791", "9")
L_PRICE = _POST % ("224254339503", "9")
L_KAMS = _POST % ("224314892182", "6")
L_DHP = _POST % ("224478710044", "6")
L_PROMO = _POST % ("224457919290", "6")
L_VIDEO = "https://youtu.be/yEiUgmcq7kw?si=12W8Q1HMyNOKfYzW"
L_MAP = "https://naver.me/FgHDoDqj"
TEL = "010-6574-1598"
L_TEL = "tel:01065741598"
MAIL = "rsvn@h-kitchen.co.kr"
L_MAIL = "mailto:rsvn@h-kitchen.co.kr?subject=%5B%ED%94%8C%EB%A0%8C%ED%8B%B0%EC%BB%A8%EB%B2%A4%EC%85%98%5D%20%ED%96%89%EC%82%AC%20%EC%83%81%EB%8B%B4%20%C2%B7%20%EA%B2%AC%EC%A0%81%20%EB%AC%B8%EC%9D%98"
L_UNSUB = "mailto:rsvn@h-kitchen.co.kr?subject=%EB%89%B4%EC%8A%A4%EB%A0%88%ED%84%B0%20%EC%88%98%EC%8B%A0%EA%B1%B0%EB%B6%80"

T = '<table role="presentation" cellpadding="0" cellspacing="0" border="0"'


def img(name):
    return BASE + "images/" + name


def eyebrow(text, color, align="center"):
    pad = "padding-left:4px;" if align == "center" else ""
    return (
        '<p class="en" style="margin:0; %sfont-family:%s; font-size:13px; line-height:18px; '
        'letter-spacing:4px; font-weight:600; color:%s; text-transform:uppercase;">%s</p>'
        % (pad, EN, color, text)
    )


def rule(color, width=36, pad="18px 0 18px 0", align="center"):
    return (
        '%s align="%s" style="margin:0 auto;"><tr><td style="padding:%s;">'
        '%s width="%d"><tr><td height="1" bgcolor="%s" style="height:1px; line-height:1px; font-size:1px; background-color:%s;">&nbsp;</td></tr></table>'
        "</td></tr></table>" % (T, align, pad, T, width, color, color)
    )


def button(label, href, fg, bg, border):
    return (
        '%s width="100%%" style="border-collapse:separate;"><tr>'
        '<td class="btn-td" align="center" bgcolor="%s" style="background-color:%s; border:1px solid %s;">'
        '<a href="%s" target="_blank" class="ko" style="display:block; padding:15px 8px; font-family:%s; font-size:14px; '
        'line-height:20px; font-weight:700; letter-spacing:0.5px; color:%s; text-decoration:none;">%s&nbsp;&nbsp;&rarr;</a>'
        "</td></tr></table>" % (T, bg, bg, border, href, KO, fg, label)
    )


def text_link(label, href, color):
    return (
        '<a href="%s" target="_blank" class="ko" style="font-family:%s; font-size:13px; line-height:20px; font-weight:700; '
        'letter-spacing:0.5px; color:%s; text-decoration:none; border-bottom:1px solid %s; padding-bottom:2px;">%s&nbsp;&nbsp;&rarr;</a>'
        % (href, KO, color, color, label)
    )


# ── sections ──────────────────────────────────────────────────────────────
def top_strip():
    return """
          <tr>
            <td class="px" bgcolor="{IVORY}" style="padding:15px 44px 13px 44px; background-color:{IVORY};">
              {T} width="100%"><tr>
                <td align="left" class="en" style="font-family:{EN}; font-size:13px; line-height:18px; letter-spacing:4px; font-weight:600; color:{G};">NEWSLETTER</td>
                <td align="right" class="en" style="font-family:{EN}; font-size:13px; line-height:18px; letter-spacing:3px; font-weight:600; color:{GOLD};">NOVEMBER 2026</td>
              </tr></table>
            </td>
          </tr>"""


def masthead():
    return """
          <tr>
            <td align="center" bgcolor="{G}" style="padding:48px 20px 40px 20px; background-color:{G};">
              {T} align="center" style="margin:0 auto;">
                <tr><td align="center" style="padding-bottom:16px;">
                  <a href="{L_HOME}" target="_blank"><img src="{IMG_EMBLEM}" width="46" height="40" alt="" style="display:block; width:46px; height:40px; margin:0 auto;" /></a>
                </td></tr>
                <tr><td align="center" class="en" style="padding-left:15px; font-family:{EN}; font-size:40px; line-height:44px; letter-spacing:15px; font-weight:500; color:{ON_G};">
                  <a href="{L_HOME}" target="_blank" style="color:{ON_G}; text-decoration:none;">PLENTY</a>
                </td></tr>
                <tr><td align="center" class="en" style="padding:8px 0 0 7px; font-family:{EN}; font-size:12px; line-height:16px; letter-spacing:7px; font-weight:600; color:{GOLD_L};">
                  <a href="{L_HOME}" target="_blank" style="color:{GOLD_L}; text-decoration:none;">CONVENTION</a>
                </td></tr>
              </table>
            </td>
          </tr>"""


def hero():
    return """
          <tr>
            <td bgcolor="{G}" style="padding:0; line-height:0; font-size:0; background-color:{G};">
              <a href="{L_HOME}" target="_blank"><img class="fluid" src="{IMG_HERO}" width="640" height="390" alt="플렌티컨벤션 홀 전경" style="display:block; width:640px; max-width:100%; height:auto;" /></a>
            </td>
          </tr>
          <tr>
            <td class="px" align="center" bgcolor="{G}" style="padding:4px 44px 58px 44px; background-color:{G};">
              {EB_HERO}
              <h1 class="ko h1" style="margin:16px 0 0 0; font-family:{KO}; font-size:31px; line-height:46px; font-weight:700; letter-spacing:-0.3px; color:{ON_G};">행사의 품격을 완성하는 공간</h1>
              {RULE_GOLD_L}
              <p class="ko" style="margin:0; font-family:{KO}; font-size:18px; line-height:30px; font-weight:700; color:{GOLD_L};">호텔의 격식은 그대로, 비용은 합리적으로.</p>
              <p class="ko" style="margin:14px 0 0 0; font-family:{KO}; font-size:15px; line-height:29px; color:{ON_G};">학회 &middot; 세미나 &middot; 기업행사까지<br />공간 &middot; 식사 &middot; 운영을 한 번에 준비합니다.</p>
              <p class="ko" style="margin:26px 0 0 0; font-family:{KO}; font-size:13px; line-height:22px; color:{ON_G_SOFT};">서울 서초 고속터미널역<!--[if !mso]><!--><br class="m-only" style="display:none;" /><!--<![endif]--><span class="m-hide">&nbsp;&nbsp;|&nbsp;&nbsp;</span>가톨릭대학교 서울성모병원 옴니버스파크</p>
            </td>
          </tr>"""


def capacity_cell(num, ko, en, last=False):
    border = "" if last else " border-right:1px solid %s;" % LINE
    return (
        '<td align="center" valign="top" width="33%%" style="padding:4px 0 2px 0;%s">'
        '<p class="en" style="margin:0; font-family:%s; font-size:58px; line-height:58px; font-weight:500; color:%s;">%s</p>'
        '<p class="ko" style="margin:8px 0 0 0; font-family:%s; font-size:15px; line-height:22px; font-weight:700; color:%s;">%s</p>'
        '<p class="en" style="margin:2px 0 0 0; padding-left:3px; font-family:%s; font-size:12px; line-height:16px; letter-spacing:3px; font-weight:600; color:%s;">%s</p>'
        "</td>" % (border, EN, G, num, KO, INK, ko, EN, GOLD, en)
    )


def photo_cell(name, alt, en, ko, href):
    return (
        '<td class="col col-pad" valign="top" width="264">'
        '<a href="%s" target="_blank"><img class="fluid" src="%s" width="264" height="198" alt="%s" style="display:block; width:264px; max-width:100%%; height:auto;" /></a>'
        '<p style="margin:12px 0 0 0;"><span class="en" style="font-family:%s; font-size:19px; line-height:24px; font-style:italic; font-weight:500; color:%s;">%s</span>'
        '<span class="ko" style="font-family:%s; font-size:13px; line-height:24px; color:%s;">&nbsp;&nbsp;%s</span></p>'
        "</td>" % (href, img(name), alt, EN, G, en, KO, MUTE, ko)
    )


GAP = '<td class="gapcol" width="24" style="width:24px; font-size:1px; line-height:1px;">&nbsp;</td>'
GAP_S = '<td class="gapcol" width="18" style="width:18px; font-size:1px; line-height:1px;">&nbsp;</td>'


def space():
    caps = capacity_cell("672", "극장식", "THEATER") + capacity_cell("360", "클래스룸", "CLASSROOM") + capacity_cell("320", "연회식", "BANQUET", last=True)
    photos = (
        photo_cell("space-banquet.jpg", "연회식 세팅으로 진행된 행사", "Banquet", "연회 &middot; 만찬", L_SPACE)
        + GAP
        + photo_cell("space-lobby.jpg", "로비 전시 부스 운영 모습", "Lobby", "리셉션 &middot; 전시 부스", L_SPACE)
    )
    b1 = button("공간 운영 안내", L_SPACE, G, IVORY, G)
    b2 = button("대관료 안내", L_PRICE, G, IVORY, G)
    b3 = button("대관 가능일", L_SCHEDULE, ON_G, G, G)
    return """
          <tr>
            <td class="px" align="center" bgcolor="{IVORY}" style="padding:60px 44px 0 44px; background-color:{IVORY};">
              {EB_SPACE}
              <h2 class="ko h2" style="margin:12px 0 0 0; font-family:{KO}; font-size:25px; line-height:38px; font-weight:700; letter-spacing:-0.3px; color:{G};">하나의 홀, 세 가지 구성</h2>
              <p class="ko" style="margin:10px 0 0 0; font-family:{KO}; font-size:14px; line-height:26px; color:{MUTE};">행사 형태에 맞춰 좌석과 테이블을 구성해 드립니다.</p>
            </td>
          </tr>
          <tr>
            <td class="px" bgcolor="{IVORY}" style="padding:34px 44px 0 44px; background-color:{IVORY};">
              {T} width="100%" style="border-top:1px solid {LINE}; border-bottom:1px solid {LINE};"><tr><td style="padding:26px 0 24px 0;">
                {T} width="100%"><tr>""" + caps + """</tr></table>
              </td></tr></table>
              <p class="ko" style="margin:12px 0 0 0; font-family:{KO}; font-size:12px; line-height:18px; color:{MUTE}; text-align:center;">최대 수용 인원 기준 &middot; 단위 명</p>
            </td>
          </tr>
          <tr>
            <td class="px" bgcolor="{IVORY}" style="padding:30px 44px 0 44px; background-color:{IVORY};">
              {T} width="100%"><tr>""" + photos + """</tr></table>
            </td>
          </tr>
          <tr>
            <td class="px" bgcolor="{IVORY}" style="padding:36px 44px 64px 44px; background-color:{IVORY};">
              {T} width="100%"><tr>
                <td class="col col-btn" valign="top" width="172">""" + b1 + """</td>""" + GAP_S + """
                <td class="col col-btn" valign="top" width="172">""" + b2 + """</td>""" + GAP_S + """
                <td class="col" valign="top" width="172">""" + b3 + """</td>
              </tr></table>
            </td>
          </tr>"""


def feature_cell(no, title, desc):
    return (
        '<td class="col" valign="top" width="264" style="border-top:1px solid %s; padding:20px 0 24px 0;">'
        '%s width="100%%"><tr>'
        '<td valign="top" width="48" class="en" style="width:48px; font-family:%s; font-size:25px; line-height:26px; font-style:italic; font-weight:500; color:%s;">%s</td>'
        '<td valign="top">'
        '<p class="ko" style="margin:0; font-family:%s; font-size:16px; line-height:26px; font-weight:700; color:%s;">%s</p>'
        '<p class="ko" style="margin:3px 0 0 0; font-family:%s; font-size:13px; line-height:22px; color:%s;">%s</p>'
        "</td></tr></table></td>" % (G_LINE, T, EN, GOLD_L, no, KO, ON_G, title, KO, ON_G_SOFT, desc)
    )


def features():
    items = [
        ("01", "초대형 LED 연출", "13m &times; 4.5m 초고화질 미디어월"),
        ("02", "단독 대관", "한 홀 전체를 단독으로 사용"),
        ("03", "올인원 행사 운영", "대관 &middot; 식사 &middot; 운영 통합 제공"),
        ("04", "다양한 테이블 세팅", "행사 목적에 따른 공간 구성"),
        ("05", "넉넉한 주차 환경", "주차 공간 200대 보유"),
        ("06", "멀티 로비 공간", "리셉션 &middot; 부스 설치 가능"),
    ]
    rows = ""
    for i in range(0, 6, 2):
        rows += "<tr>" + feature_cell(*items[i]) + GAP + feature_cell(*items[i + 1]) + "</tr>"
    return """
          <tr>
            <td class="px" align="center" bgcolor="{G}" style="padding:60px 44px 0 44px; background-color:{G};">
              {EB_WHY}
              <h2 class="ko h2" style="margin:12px 0 0 0; font-family:{KO}; font-size:25px; line-height:38px; font-weight:700; letter-spacing:-0.3px; color:{ON_G};">준비가 가벼워지는 여섯 가지</h2>
            </td>
          </tr>
          <tr>
            <td class="px" bgcolor="{G}" style="padding:34px 44px 0 44px; background-color:{G};">
              {T} width="100%">""" + rows + """</table>
            </td>
          </tr>
          <tr>
            <td class="px" align="center" bgcolor="{G}" style="padding:14px 44px 60px 44px; background-color:{G}; border-top:0;">
              """ + text_link("공간 운영 안내 자세히 보기", L_SPACE, GOLD_L) + """
            </td>
          </tr>"""


def story_cell(name, alt, kicker, title, href):
    return (
        '<td class="col col-pad" valign="top" width="264">'
        '<a href="%s" target="_blank"><img class="fluid" src="%s" width="264" height="198" alt="%s" style="display:block; width:264px; max-width:100%%; height:auto;" /></a>'
        '<p class="en" style="margin:16px 0 0 0; font-family:%s; font-size:12px; line-height:16px; letter-spacing:3px; font-weight:600; color:%s;">%s</p>'
        '<p class="ko" style="margin:6px 0 12px 0; font-family:%s; font-size:17px; line-height:27px; font-weight:700; color:%s;"><a href="%s" target="_blank" style="color:%s; text-decoration:none;">%s</a></p>'
        "%s</td>" % (href, img(name), alt, EN, GOLD, kicker, KO, G, href, G, title, text_link("현장 보기", href, G))
    )


def stories():
    cells = (
        story_cell("story-kams.jpg", "2026 대한의학회 학술대회 현장", "ACADEMIC CONGRESS", "2026 대한의학회 학술대회", L_KAMS)
        + GAP
        + story_cell("story-dhp.jpg", "2026 DHP 컨퍼런스 현장", "CONFERENCE", "2026 DHP 컨퍼런스", L_DHP)
    )
    return """
          <tr>
            <td class="px" align="center" bgcolor="{IVORY}" style="padding:60px 44px 0 44px; background-color:{IVORY};">
              {EB_STORY}
              <h2 class="ko h2" style="margin:12px 0 0 0; font-family:{KO}; font-size:25px; line-height:38px; font-weight:700; letter-spacing:-0.3px; color:{G};">사진으로 만나는 행사 현장</h2>
            </td>
          </tr>
          <tr>
            <td class="px" bgcolor="{IVORY}" style="padding:34px 44px 56px 44px; background-color:{IVORY};">
              {T} width="100%"><tr>""" + cells + """</tr></table>
            </td>
          </tr>"""


def video():
    return """
          <tr>
            <td class="px" bgcolor="{IVORY}" style="padding:0 44px 0 44px; background-color:{IVORY};">
              {T} width="100%"><tr><td height="1" bgcolor="{LINE}" style="height:1px; line-height:1px; font-size:1px; background-color:{LINE};">&nbsp;</td></tr></table>
            </td>
          </tr>
          <tr>
            <td class="px" align="center" bgcolor="{IVORY}" style="padding:56px 44px 0 44px; background-color:{IVORY};">
              {EB_VIDEO}
              <h2 class="ko h2" style="margin:12px 0 0 0; font-family:{KO}; font-size:25px; line-height:38px; font-weight:700; letter-spacing:-0.3px; color:{G};">2027 서울 세계청년대회(WYD)<br />사전행사 콘서트</h2>
              <p class="ko" style="margin:10px 0 0 0; font-family:{KO}; font-size:14px; line-height:26px; color:{MUTE};">2026년에 열린 사전행사의 특별한 순간을<!--[if !mso]><!--><br class="m-only" style="display:none;" /><!--<![endif]--> 영상으로 만나 보세요.</p>
            </td>
          </tr>
          <tr>
            <td class="px" align="center" bgcolor="{IVORY}" style="padding:30px 44px 0 44px; background-color:{IVORY};">
              <a href="{L_VIDEO}" target="_blank"><img class="fluid" src="{IMG_VIDEO}" width="552" height="310" alt="젠베르데, 평화를 노래하다 – 영상 보기" style="display:block; width:552px; max-width:100%; height:auto;" /></a>
            </td>
          </tr>
          <tr>
            <td class="px" align="center" bgcolor="{IVORY}" style="padding:20px 44px 64px 44px; background-color:{IVORY};">
              """ + text_link("영상 보기", L_VIDEO, G) + """
            </td>
          </tr>"""


def benefit_cell(no, line1, line2, last=False):
    border = "" if last else " border-right:1px solid %s;" % LINE
    return (
        '<td class="col col-benefit" align="center" valign="top" width="33%%" style="padding:2px 6px 2px 6px;%s">'
        '<p class="en" style="margin:0; font-family:%s; font-size:22px; line-height:26px; font-style:italic; font-weight:500; color:%s;">%s</p>'
        '<p class="ko" style="margin:8px 0 0 0; font-family:%s; font-size:15px; line-height:24px; font-weight:700; color:%s;">%s<br />%s</p>'
        "</td>" % (border, EN, GOLD, no, KO, INK, line1, line2)
    )


def promotion():
    benefits = (
        benefit_cell("i.", "대관료", "특별 할인")
        + benefit_cell("ii.", "13m LED 미디어월", "이용료 할인")
        + benefit_cell("iii.", "커피브레이크", "할인", last=True)
    )
    return """
          <tr>
            <td class="px-s" bgcolor="{G}" style="padding:44px 28px 44px 28px; background-color:{G};">
              {T} width="100%" style="border-collapse:separate;"><tr>
                <td bgcolor="{PAPER}" style="padding:6px; background-color:{PAPER};">
                  {T} width="100%" style="border-collapse:separate;"><tr>
                    <td class="card" align="center" style="border:1px solid {GOLD}; padding:46px 30px 44px 30px;">
                      {EB_PROMO}
                      <h2 class="ko h2" style="margin:14px 0 0 0; font-family:{KO}; font-size:27px; line-height:40px; font-weight:800; letter-spacing:-0.3px; color:{G};">학회 &middot; 세미나 &middot; 기업행사<br />프로모션</h2>
                      {RULE_GOLD}
                      <p class="ko" style="margin:0; font-family:{KO}; font-size:21px; line-height:30px; font-weight:700; letter-spacing:1px; color:{G};">1월 &middot; 2월 &middot; 7월 &middot; 8월</p>
                      <p class="en" style="margin:6px 0 0 0; padding-left:3px; font-family:{EN}; font-size:12px; line-height:16px; letter-spacing:3px; font-weight:600; color:{GOLD};">JAN &middot; FEB &middot; JUL &middot; AUG 2027</p>
                      {T} width="100%" style="margin:0;"><tr><td style="padding:30px 0 0 0;">
                        {T} width="100%" style="border-top:1px solid {LINE}; border-bottom:1px solid {LINE};"><tr><td style="padding:22px 0 22px 0;">
                          {T} width="100%"><tr>""" + benefits + """</tr></table>
                        </td></tr></table>
                      </td></tr></table>
                      {T} align="center" style="margin:0 auto;"><tr><td style="padding:30px 0 0 0;">
                        {T} width="248" style="border-collapse:separate;"><tr>
                          <td class="btn-td" align="center" bgcolor="{G}" style="background-color:{G}; border:1px solid {G};">
                            <a href="{L_PROMO}" target="_blank" class="ko" style="display:block; padding:15px 8px; font-family:{KO}; font-size:14px; line-height:20px; font-weight:700; letter-spacing:0.5px; color:{ON_G}; text-decoration:none;">프로모션 자세히 보기&nbsp;&nbsp;&rarr;</a>
                          </td>
                        </tr></table>
                      </td></tr></table>
                      <p class="ko" style="margin:18px 0 0 0; font-family:{KO}; font-size:13px; line-height:22px; color:{MUTE};">대관 상담 및 일정 문의&nbsp;&nbsp;<a href="{L_TEL}" class="en" style="font-family:{EN}; font-size:19px; letter-spacing:1px; color:{G}; font-weight:600; text-decoration:none;">{TEL}</a></p>
                    </td>
                  </tr></table>
                </td>
              </tr></table>
            </td>
          </tr>"""


def contact_row(label, value, last=False):
    border = "" if last else " border-bottom:1px solid %s;" % LINE
    return (
        "<tr>"
        '<td class="ko" width="64" valign="top" style="width:64px; padding:13px 0 13px 0;%s font-family:%s; font-size:13px; line-height:22px; color:%s;">%s</td>'
        '<td class="ko" valign="top" style="padding:13px 0 13px 0;%s font-family:%s; font-size:15px; line-height:22px; font-weight:700; color:%s;">%s</td>'
        "</tr>" % (border, KO, MUTE, label, border, KO, G, value)
    )


def reservation():
    rows = (
        contact_row("담당", "플렌티컨벤션 연회예약")
        + contact_row("전화", '<a href="%s" class="en" style="font-family:%s; font-size:20px; letter-spacing:1px; color:%s; text-decoration:none;">%s</a>' % (L_TEL, EN, G, TEL))
        + contact_row("메일", '<a href="%s" class="en" style="font-family:%s; font-size:20px; letter-spacing:0.5px; color:%s; text-decoration:none;">%s</a>' % (L_MAIL, EN, G, MAIL), last=True)
    )
    b_mail = button("메일로 견적 문의", L_MAIL, G, ON_G, ON_G)
    b_date = button("대관 가능일 확인", L_SCHEDULE, ON_G, G, GOLD_L)
    return """
          <tr>
            <td class="px" align="center" bgcolor="{G}" style="padding:20px 44px 0 44px; background-color:{G};">
              {EB_RSVN}
              <h2 class="ko h2" style="margin:12px 0 0 0; font-family:{KO}; font-size:27px; line-height:40px; font-weight:700; letter-spacing:-0.3px; color:{ON_G};">다음 행사, 함께 준비하세요.</h2>
              {RULE_GOLD_L}
              <p class="ko" style="margin:0; font-family:{KO}; font-size:15px; line-height:29px; color:{ON_G};">희망 일정 &middot; 예상 인원 &middot; 행사 형태를 알려주시면<br />가능한 일정과 견적을 안내드립니다.<br />현장 답사도 편하게 문의해 주세요.</p>
            </td>
          </tr>
          <tr>
            <td class="px" bgcolor="{G}" style="padding:34px 44px 0 44px; background-color:{G};">
              {T} width="100%"><tr>
                <td bgcolor="{PAPER}" style="padding:12px 30px 12px 30px; background-color:{PAPER};">
                  {T} width="100%">""" + rows + """</table>
                </td>
              </tr></table>
            </td>
          </tr>
          <tr>
            <td class="px" bgcolor="{G}" style="padding:18px 44px 64px 44px; background-color:{G};">
              {T} width="100%"><tr>
                <td class="col col-btn" valign="top" width="267">""" + b_mail + """</td>""" + GAP_S + """
                <td class="col" valign="top" width="267">""" + b_date + """</td>
              </tr></table>
            </td>
          </tr>"""


def footer():
    link = 'style="color:%s; text-decoration:none;"' % GOLD_L
    return """
          <tr>
            <td class="px" align="center" bgcolor="{G_DEEP}" style="padding:40px 44px 44px 44px; background-color:{G_DEEP};">
              <p class="en" style="margin:0; padding-left:4px; font-family:{EN}; font-size:14px; line-height:20px; letter-spacing:4px; font-weight:600; color:{GOLD_L};">PLENTY CONVENTION</p>
              <p class="ko" style="margin:12px 0 0 0; font-family:{KO}; font-size:13px; line-height:23px; color:{ON_G_SOFT};">플렌티컨벤션<br />서울특별시 서초구 반포대로 222<!--[if !mso]><!--><br class="m-only" style="display:none;" /><!--<![endif]--><span class="m-hide"> &middot; </span>가톨릭대학교 성의교정 옴니버스파크 로비층(L)<br /><a href="{L_TEL}" class="en" style="font-family:{EN}; font-size:16px; letter-spacing:1px; color:{ON_G_SOFT}; text-decoration:none;">{TEL}</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="{L_MAIL}" class="en" style="font-family:{EN}; font-size:16px; letter-spacing:0.5px; color:{ON_G_SOFT}; text-decoration:none;">{MAIL}</a></p>
              <p class="ko" style="margin:20px 0 0 0; font-family:{KO}; font-size:13px; line-height:22px; font-weight:700; color:{GOLD_L};">
                <a href="{L_HOME}" target="_blank" """ + link + """>홈페이지</a>&nbsp;&nbsp;&nbsp;&middot;&nbsp;&nbsp;&nbsp;<a href="{L_BLOG}" target="_blank" """ + link + """>블로그</a>&nbsp;&nbsp;&nbsp;&middot;&nbsp;&nbsp;&nbsp;<a href="{L_MAP}" target="_blank" """ + link + """>오시는 길</a>
              </p>
              {T} width="100%"><tr><td style="padding:26px 0 0 0;">
                {T} width="100%"><tr><td height="1" bgcolor="{G_LINE}" style="height:1px; line-height:1px; font-size:1px; background-color:{G_LINE};">&nbsp;</td></tr></table>
              </td></tr></table>
              <p class="ko" style="margin:20px 0 0 0; font-family:{KO}; font-size:12px; line-height:20px; color:#8a9a8f;">본 메일은 플렌티컨벤션에 행사 문의를 주신 분들께 발송됩니다.<br />수신을 원하지 않으시면 <a href="{L_UNSUB}" style="color:#8a9a8f; text-decoration:underline;">수신거부</a>를 눌러 주세요.</p>
            </td>
          </tr>"""


HEAD = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="ko">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="x-apple-disable-message-reformatting" />
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no" />
  <meta name="color-scheme" content="light only" />
  <meta name="supported-color-schemes" content="light only" />
  <title>PLENTY CONVENTION Newsletter | 행사의 품격을 완성하는 공간</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&amp;family=Nanum+Myeongjo:wght@400;700;800&amp;display=swap" />
  <!--[if mso]>
  <noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
  <style type="text/css">
    table, td, p, a, span, h1, h2 { text-autospace: none !important; }
    td, p, h1, h2 { mso-line-height-rule: exactly; }
    .en, .en a { font-family: Georgia, 'Times New Roman', serif !important; }
    .ko, .ko a { font-family: 'Batang', '바탕', Georgia, serif !important; mso-fareast-font-family: 'Batang'; }
    .btn-td { padding: 15px 8px !important; }
  </style>
  <![endif]-->
  <style type="text/css">
    @import url('https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Nanum+Myeongjo:wght@400;700;800&display=swap');
    :root { color-scheme: light only; supported-color-schemes: light only; }
    body { margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
    table { border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
    img { border: 0; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }
    a { text-decoration: none; }
    h1, h2, p { margin: 0; }
    .en { font-variant-numeric: lining-nums; -webkit-font-feature-settings: 'lnum'; font-feature-settings: 'lnum'; }
    @media only screen and (max-width: 660px) {
      .wrapper { width: 100% !important; }
      .fluid { width: 100% !important; height: auto !important; }
      .px { padding-left: 24px !important; padding-right: 24px !important; }
      .px-s { padding-left: 14px !important; padding-right: 14px !important; }
      .card { padding-left: 18px !important; padding-right: 18px !important; }
      .col { display: block !important; width: 100% !important; box-sizing: border-box; }
      .col-pad { padding-bottom: 30px !important; }
      .col-btn { padding-bottom: 12px !important; }
      .col-benefit { border-right: 0 !important; padding-top: 12px !important; padding-bottom: 12px !important; }
      .gapcol { display: none !important; }
      .h1 { font-size: 26px !important; line-height: 40px !important; }
      .h2 { font-size: 22px !important; line-height: 34px !important; }
      .m-only { display: inline !important; }
      .m-hide { display: none !important; }
    }
  </style>
</head>
<body bgcolor="#ffffff" style="margin:0; padding:0; background-color:#ffffff;">

  <div style="display:none; font-size:1px; color:#ffffff; line-height:1px; max-height:0; max-width:0; opacity:0; overflow:hidden; mso-hide:all;">
    호텔의 격식은 그대로, 비용은 합리적으로. 2027년 학회 · 세미나 · 기업행사 프로모션과 대관 가능일을 안내드립니다.
  </div>

  {T} width="100%" bgcolor="#ffffff" style="background-color:#ffffff;">
    <tr>
      <td align="center" style="padding:0;">
        <!--[if (gte mso 9)|(IE)]>
        <table role="presentation" width="640" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td>
        <![endif]-->
        {T} class="wrapper" width="640" bgcolor="{IVORY}" style="width:640px; max-width:640px; background-color:{IVORY};">
"""

TAIL = """
        </table>
        <!--[if (gte mso 9)|(IE)]>
        </td></tr></table>
        <![endif]-->
      </td>
    </tr>
  </table>

</body>
</html>
"""


def build():
    body = HEAD + top_strip() + masthead() + hero() + space() + features() + stories() + video() + promotion() + reservation() + footer() + TAIL
    values = {
        "T": T, "EN": EN, "KO": KO, "G": G, "G_DEEP": G_DEEP, "G_LINE": G_LINE, "IVORY": IVORY, "PAPER": PAPER,
        "LINE": LINE, "GOLD": GOLD, "GOLD_L": GOLD_L, "INK": INK, "MUTE": MUTE, "ON_G": ON_G, "ON_G_SOFT": ON_G_SOFT,
        "L_HOME": L_HOME, "L_SCHEDULE": L_SCHEDULE, "L_BLOG": L_BLOG, "L_SPACE": L_SPACE, "L_PRICE": L_PRICE,
        "L_PROMO": L_PROMO, "L_VIDEO": L_VIDEO, "L_MAP": L_MAP, "L_TEL": L_TEL, "TEL": TEL, "L_MAIL": L_MAIL,
        "MAIL": MAIL, "L_UNSUB": L_UNSUB,
        "IMG_EMBLEM": img("emblem.png"), "IMG_HERO": img("hero.jpg"), "IMG_VIDEO": img("video-wyd.jpg"),
        "EB_HERO": eyebrow("Premium Convention &middot; Seoul", GOLD_L),
        "EB_SPACE": eyebrow("The Space", GOLD),
        "EB_WHY": eyebrow("Why Plenty", GOLD_L),
        "EB_STORY": eyebrow("Event Story", GOLD),
        "EB_VIDEO": eyebrow("Video Story", GOLD),
        "EB_PROMO": eyebrow("2027 MICE Special Promotion", GOLD),
        "EB_RSVN": eyebrow("Reservation", GOLD_L),
        "RULE_GOLD": rule(GOLD),
        "RULE_GOLD_L": rule(GOLD_L),
    }
    for key, val in values.items():
        body = body.replace("{" + key + "}", val)
    left = [tok for tok in ("{EN}", "{KO}", "{T}", "{G}") if tok in body]
    assert not left, left
    out_dir = ISSUE
    with io.open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    with io.open(os.path.join(out_dir, "_preview.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(body.replace(BASE, ""))
    print("built", out_dir, len(body), "bytes")


build()
