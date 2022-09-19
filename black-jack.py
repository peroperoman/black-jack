import random

class Player():
    def __init__(self, name, is_dealer=False, is_max=21):
        self.name = name
        self.deck = []
        self.total = 0
        self.is_dealer = is_dealer
        self.is_max = is_max

    def __repr__(self):
        return self.name


class Dealer():
    def __init__(self, *args):
        self.deck = self.init_deck()
        self.players = self.init_deal(*args)

    def init_deck(self) -> list:
        marks = ['ダイヤ', 'クラブ', 'ハート', 'スペード']
        values = [i for i in range(2, 11)] + ['A', 'J', 'Q', 'K']
        deck = [[mark, value] for mark in marks for value in values]
        random.shuffle(deck)
        return deck

    def init_deal(self, *args) -> list:
        players = list(args)
        for player in players:
            player.deck = [self.deck.pop() for _ in range(2)]
        return players


class BlackJack():
    def __init__(self, players, deck):
        self.point_d = {'A': 1, 'J': 10, 'Q': 10, 'K': 10}
        self.players = players
        self.deck = deck
        self.update_total(0)
        self.update_total(1)
        self.farst_display()

    def farst_display(self):
        r = [[player.name, player.deck , player.total] for player in self.players]
        print(r[1][0] + ' のカード -> ' , r[1][1][0])
        print(r[0][0] + ' のカード -> ' , *r[0][1] , '=' , '合計:' , r[0][2])

    def update_total(self, idx) -> int:
        self.players[idx].total = 0
        for card in self.players[idx].deck:
            self.players[idx].total += self.point_d[card[1]] if card[1] in ['A', 'J', 'Q', 'K'] else card[1]

    def player_display(self, idx):
        r = [self.players[idx].name , self.players[idx].deck , self.players[idx].total]
        print(r[0] + ' のカード -> ' , *r[1] , '=' , '合計:' , r[2])

    def burst_display(self, idx):
        print(f'\n{self.players[idx].name} はバーストしました')
        if self.players[idx].is_dealer:
            print(f'\n{self.players[0].name} の勝ち! \n')
        else:
            print(f'{self.players[idx].name} は負けました・・・ \n')

    def draw_card(self, idx):
        while True:
            if not self.players[idx].is_dealer:
                tmp = str(input('カードを引きますか？ y/n : '))
                draw_sts = True if tmp == 'y' else False

            if (self.players[idx].is_dealer
                and self.players[idx].total >= self.players[idx].is_max):
                break

            if self.players[idx].is_dealer or draw_sts:
                self.players[idx].deck.append(self.deck.pop(0))
                self.update_total(idx)
                self.player_display(idx)
            else:
                break

            if self.players[idx].total > 21:
                self.burst_display(idx)
                exit()

    def win_judgment(self):
        self.update_total(0)
        self.update_total(1)
        print('\n' + '-'*20 + '結果' + '-'*20)
        self.player_display(0)
        self.player_display(1)
        if self.players[1].total == self.players[0].total:
            print('\n引き分け・・・\n')
        elif self.players[1].total > self.players[0].total:
            print(f'\n{self.players[0].name} は負けました・・・ \n')
        elif self.players[1].total < self.players[0].total:
            print(f'\n{self.players[0].name} の勝ち! \n')

def game_start():
    you = Player('You')
    cpu = Player('Dealer', is_dealer=True, is_max=17)
    dealer = Dealer(you, cpu)
    bj = BlackJack(dealer.players, dealer.deck)
    bj.draw_card(0)
    bj.draw_card(1)
    bj.win_judgment()

def main():
    game_start()

if __name__ == '__main__':
    main()
