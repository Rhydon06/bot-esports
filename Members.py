import json
import os

# Members というクラスを定義 (メソッドと変数の集まりみたいな)
# 外側からは Members() でインスタンス化できる。
class Members:
    # インスタンス化するときに自動的に実行される。
    # selfはおまじないみたいなもの
    # self.変数 で Membersが持つ変数になる
    # self.関数 で Membersが持つ関数になる
    def __init__(self, file_name):
        self.file_name = file_name
        if not os.path.exists(file_name):
            self.write_members({})
        else:
            self.members = self.read_members()

    # ファイルを読み込む。
    # 読み込んだ結果を辞書型で返す

    def read_members(self) -> dict:
        with open(self.file_name, "r") as f:
            members = json.load(f)
        return members
    
# ファイルを書き込むだけ
    def write_members(self, new_members): ##これは使ってない##
        with open(self.file_name, "w") as f: # 書き込みモードでファイルを読み込み
            json.dump(new_members, f, ensure_ascii=False, indent=2)  # JSONファイルへの書き込み

# 値を更新してからファイルを書き込む
    def add_member(self, new_member):
        member = self.read_members() # 既存の会員データを読み込み
        member.update(new_member)    # 新しい会員を追加
        self.write_members(member)   # 更新された会員データを書き込み
