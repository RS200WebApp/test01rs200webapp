#!/usr/bin/env python
#coding: utf-8
import os
import webapp2
import jinja2
import logging
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class UserData(ndb.Model):
    name = ndb.StringProperty()
    time = ndb.IntegerProperty()
    team = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class BaseHandler(webapp2.RequestHandler):
    def render(self, html, values={}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))

    def post(self):
        POKEMONLIST = (u'キモリ', u'ジュプトル', u'ジュカイン', u'アチャモ', u'ワカシャモ', u'バシャーモ', u'ミズゴロウ', u'ヌマクロー', u'ラグラージ', u'ポチエナ', u'グラエナ', u'ジグザグマ', u'マッスグマ', u'ケムッソ', u'カラサリス', u'アゲハント', u'マユルド', u'ドクケイル', u'ハスボー', u'ハスブレロ', u'ルンパッパ', u'タネボー', u'コノハナ',u'ダーテング',u'スバメ',u'オオスバメ',u'キャモメ',u'ペリッパー',u'ラルトス',u'キルリア',u'サーナイト',u'アメタマ',u'アメモース',u'キノココ',u'キノガッサ',u'ナマケロ',u'ヤルキモノ',u'ケッキング',u'ケーシィ',u'ユンゲラー',u'フーディン',u'ツチニン',u'テッカニン',u'ヌケニン',u'ゴニョニョ',u'ドゴーム',u'バクオング',u'マクノシタ',u'ハリテヤマ',u'トサキント',u'アズマオウ',u'コイキング',u'ギャラドス',u'ルリリ',u'マリル',u'マリルリ',u'イシツブテ',u'ゴローン',u'ゴローニャ',u'ノズパス',u'エネコ',u'エネコロロ',u'ズバット',u'ゴルバット',u'クロバット',u'メノクラゲ',u'ドククラゲ',u'ヤミラミ',u'クチート',u'ココドラ',u'コドラ',u'ボスゴドラ',u'ワンリキー',u'ゴーリキー',u'カイリキー',u'アサナン',u'チャーレム',u'ラクライ',u'ライボルト',u'プラスル',u'マイナン',u'コイル',u'レアコイル',u'ビリリダマ',u'マルマイン',u'バルビート',u'イルミーゼ',u'ナゾノクサ',u'クサイハナ',u'ラフレシア',u'キレイハナ',u'ドードー',u'ドードリオ',u'ロゼリア',u'ゴクリン',u'マルノーム',u'キバニア',u'サメハダー',u'ホエルコ',u'ホエルオー',u'ドンメル',u'バクーダ',u'マグマッグ',u'マグカルゴ',u'コータス',u'ベトベター',u'ベトベトン',u'ドガース',u'マタドガス',u'バネブー',u'ブーピッグ',u'サンド',u'サンドパン',u'パッチール',u'エアームド',u'ナックラー',u'ビブラーバ',u'フライゴン',u'サボネア',u'ノクタス',u'チルット',u'チルタリス',u'ザングース',u'ハブネーク',u'ルナトーン',u'ソルロック',u'ドジョッチ',u'ナマズン',u'ヘイガニ',u'シザリガー',u'ヤジロン',u'ネンドール',u'リリーラ',u'ユレイドル',u'アノプス',u'アーマルド',u'ププリン',u'プリン',u'プクリン',u'ヒンバス',u'ミロカロス',u'ポワルン',u'ヒトデマン',u'スターミー',u'カクレオン',u'カゲボウズ',u'ジュペッタ',u'ヨマワル',u'サマヨール',u'トロピウス',u'チリーン',u'アブソル',u'ロコン',u'キュウコン',u'ピチュー',u'ピカチュウ',u'ライチュウ',u'コダック',u'ゴルダック',u'ソーナノ',u'ソーナンス',u'ネイティ',u'ネイティオ',u'キリンリキ',u'ゴマゾウ',u'ドンファン',u'カイロス',u'ヘラクロス',u'サイホーン',u'サイドン',u'ユキワラシ',u'オニゴーリ',u'タマザラシ',u'トドグラー',u'トドゼルガ',u'パールル',u'ハンテール',u'サクラビス',u'ジーランス',u'サニーゴ',u'チョンチー',u'ランターン',u'ラブカス',u'タッツー',u'シードラ',u'キングドラ',u'タツベイ',u'コモルー',u'ボーマンダ',u'ダンバル',u'メタング',u'メタグロス',u'レジロック',u'レジアイス',u'レジスチル',u'ラティアス',u'ラティオス',u'カイオーガ',u'グラードン',u'レックウザ')
        NAMEtoPASS = {'araki':'arakigo', 
                      'hiraiwa':'hiraiwaka',
                      'yamasho':'yamashopi',
                      'matsunaga':'matsunagahe'}
        PULL_NUMBER_SOLO = 205
        #上はサイトのURLとひも付ける.今は仮にチーム名の頭文字.
        mode = self.request.get('mode')
        name = self.request.get('name')
        time_str = self.request.get('time')
        team = self.request.get('team')
        if mode == "hokaku":
            if name in POKEMONLIST:
                data1 = UserData.query(UserData.team == team)
                data = data1.filter(UserData.name == name).fetch(PULL_NUMBER_SOLO)
                #Tips:.fetchをつけることで、データ型がリストになるらしい。付けなければクエリ型
                if len(data) != 0:
                    password = NAMEtoPASS[team]
                    values = { 'pass' : password }
                    self.render('error.html', values)
                else:
                    ins = UserData()
                    ins.name = name
                    ins.time = int(time_str)
                    ins.team = team
                    ins.put()
                    self.redirect('/'+NAMEtoPASS[team])
            else:
                password = NAMEtoPASS[team]
                values = { 'pass' : password }
                self.render('error.html', values)

class MainHandler(BaseHandler):
    def get(self):
        PULL_NUMBER = 810
        araki = UserData.query(UserData.team == "araki").fetch(PULL_NUMBER)
        hiraiwa = UserData.query(UserData.team == "hiraiwa").fetch(PULL_NUMBER)
        yamasho = UserData.query(UserData.team == "yamasho").fetch(PULL_NUMBER)
        matsunaga = UserData.query(UserData.team == "matsunaga").fetch(PULL_NUMBER)
        araki_len = len(araki)
        hiraiwa_len = len(hiraiwa)
        yamasho_len = len(yamasho)
        matsunaga_len = len(matsunaga)
        values = { 'araki_get_num':araki_len, 
                   'hiraiwa_get_num':hiraiwa_len, 
                   'yamasho_get_num':yamasho_len, 
                   'matsunaga_get_num':matsunaga_len, }
        self.render('main.html', values)

class ErrorHandler(BaseHandler):
    def get(self):
        self.render('error.html')

class ArakiHandler(BaseHandler):
    def get(self):
        values = { 'pass':'arakigo', 'team':'araki' }
        self.render('register.html', values)

class HiraiwaHandler(BaseHandler):
    def get(self):
        values = { 'pass':'hiraiwaka','team':'hiraiwa' }
        self.render('register.html', values)

class YamashoHandler(BaseHandler):
    def get(self):
        values = { 'pass':'yamashopi','team':'yamasho' }
        self.render('register.html', values)

class MatsunagaHandler(BaseHandler):
    def get(self):
        values = { 'pass':'matsunagahe','team':'matsunaga' }
        self.render('register.html', values)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/error', ErrorHandler),
    ('/arakigo', ArakiHandler),
    ('/hiraiwaka', HiraiwaHandler),
    ('/yamashopi', YamashoHandler),
    ('/matsunagahe', MatsunagaHandler)
], debug=True)