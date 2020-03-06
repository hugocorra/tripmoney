import argparse
import datetime
import uuid
import json

import locale
from prettytable import PrettyTable

#locale.setlocale(locale.LC_ALL, '')
locale.setlocale(locale.LC_NUMERIC, 'English')


def float_or_none(value):
    if value is not None:
        return float(value)

    return None


def float_format(value):
    if value is not None:
        return locale.format_string('%.2f', value, True)

    return ''


class Conta(object):
    def __init__(self, *args, **kwargs):
        super(Conta, self).__init__()
        self.nome = kwargs.get('nome')
        self.moeda = kwargs.get('moeda') 

    def to_dict(self):
        obj = self.__dict__
        return obj


def new_conta():
    input_nome = input('nome: ')
    input_moeda = input('moeda: ')

    if any(not v for v in (input_nome, input_moeda)):
        raise('nova conta invalida')

    conta = Conta(
        nome=input_nome,
        moeda=input_moeda)

    return conta


def load_contas():
    with open('contas.json') as f_contas:
        l_contas_raw = json.load(f_contas)
        l_contas = []
        
        for conta in l_contas_raw:
            conta_obj = Conta(**conta)
            l_contas.append(conta_obj)

        return l_contas

    raise('nao foi possivel abrir arquivo de contas')


def save_contas(l_contas):
    l_contas_raw = []

    for conta in l_contas:
        l_contas_raw.append(conta.to_dict())

    with open('contas.json', 'w') as f_contas:
        json.dump(l_contas_raw, f_contas, sort_keys=True, indent=4)


def print_contas(l_contas):
    for c in l_contas:
        print(f'{c.nome};{c.moeda}')


class Transferencia(object):
    def __init__(self, *args, **kwargs):
        super(Transferencia, self).__init__()
        self.uuid = kwargs.get('uuid', uuid.uuid4())
        self.date = kwargs.get('date')
        self.from_acc = kwargs.get('from_acc')
        self.to_acc = kwargs.get('to_acc')
        self.value_from = float_or_none(kwargs.get('value_from'))
        self.value_to = float_or_none(kwargs.get('value_to'))
        self.gasto = kwargs.get('gasto')
        self.details = kwargs.get('details')

    def to_dict(self):
        obj = self.__dict__
        obj['uuid'] = str(self.uuid)
        return obj


def new_transferencia():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    input_date = input(f'data ({today}): ')
    input_from = input('from account: ')
    input_to = input('to account: ')
    input_value_from = input('value from: ')
    input_value_to = input('value to: ')
    input_details = input('details: ')

    if not input_date:
        input_date = today

    if any(not v for v in (input_from, input_to, input_value_from, input_value_to)):
        raise('nova transferencia invalida')

    transferencia = Transferencia(
        date=input_date,
        from_acc=input_from,
        to_acc=input_to,
        value_from=input_value_from,
        value_to=input_value_to,
        details=input_details)

    return transferencia


def load_transferencias():
    with open('transferencias.json') as f_transferencias:
        l_transferencias_raw = json.load(f_transferencias)
        l_transferencias = []
        
        for transf in l_transferencias_raw:
            trans_obj = Transferencia(**transf)
            l_transferencias.append(trans_obj)

        return l_transferencias

    raise('nao foi possivel abrir arquivo de transferencias')


def save_transferencias(l_transferencias):
    l_transferencias_raw = []

    for transf in l_transferencias:
        l_transferencias_raw.append(transf.to_dict())

    with open('transferencias.json', 'w') as f_transferencias:
        json.dump(l_transferencias_raw, f_transferencias, sort_keys=True, indent=4)


def print_transferencias(l_transferencias):
    pt = PrettyTable(['date', 'from', 'to', 'value from', 'value to', 'has gasto', 'details'])
    pt.align['value from'] = 'r'
    pt.align['value to'] = 'r'

    for t in l_transferencias:
        pt.add_row([t.date, t.from_acc, t.to_acc, float_format(t.value_from), float_format(t.value_to), bool(t.gasto), t.details])
        #print(f'{t.date};{t.from_acc};{t.to_acc};{t.value_from};{t.value_to};{t.gasto};{t.details}')

    print(pt)



class Gasto(object):
    def __init__(self, *args, **kwargs):
        super(Gasto, self).__init__()
        self.uuid = kwargs.get('uuid', uuid.uuid4())
        self.date = kwargs.get('date')
        self.pais = kwargs.get('pais')
        self.conta = kwargs.get('conta')
        self.moeda = kwargs.get('moeda')
        self.valor = float_or_none(kwargs.get('valor'))
        self.descricao = kwargs.get('descricao')
        self.categoria = kwargs.get('categoria')
        self.periodo_de = kwargs.get('periodo_de')
        self.periodo_ate = kwargs.get('periodo_ate')

    def to_dict(self):
        obj = self.__dict__
        obj['uuid'] = str(self.uuid)
        return obj


def new_gasto():
    contas_list = load_contas()
    contas = {}
    for conta in contas_list:
        contas[conta.nome] = conta.moeda

    today = datetime.datetime.today().strftime('%Y-%m-%d')
    input_date = input(f'data ({today}): ')
    input_pais = input(f'pais: ')

    input_conta = input('conta: ' )

    while not input_conta in contas:
        print('conta invalida')
        input_conta = input('conta: ' )

    input_moeda = input(f'moeda ({contas[input_conta]}): ')

    criar_transacao = False

    if not input_moeda:
        input_moeda = contas[input_conta]
    else:
        if input_moeda != contas[input_conta]:
            criar_transacao = True

    input_valor = input(f'valor em {input_moeda}: ')
    input_valor_transacao = None

    if criar_transacao:
        input_valor_transacao = input(f'valor em {contas[input_conta]}: ')

    input_descricao = input('descricao: ')
    input_categoria = input('categoria: ')
    input_periodo_de = input('periodo_de: ')
    input_periodo_ate = input('periodo_ate: ')

    if not input_date:
        input_date = today

    if any(not v for v in (input_pais, input_conta, input_valor, input_descricao)):
        raise('novo gasto invalida')

    gasto = Gasto(
        date=input_date,
        pais=input_pais,
        conta=input_conta,
        moeda=input_moeda,
        valor=input_valor,
        descricao=input_descricao,
        categoria=input_categoria,
        periodo_de=input_periodo_de,
        peridodo_ate=input_periodo_ate)

    transacao = None
    if criar_transacao:
        transacao = Transferencia(date=input_date,
            from_acc=input_conta,
            to_acc=input_moeda,
            value_from=input_valor_transacao,
            value_to=float(input_valor) * -1,
            gasto=str(gasto.uuid),
            details=input_descricao)

    return gasto, transacao


def load_gastos():
    with open('gastos.json') as f_gastos:
        l_gastos_raw = json.load(f_gastos)
        l_gastos = []
        
        for gasto in l_gastos_raw:
            gasto_obj = Gasto(**gasto)
            l_gastos.append(gasto_obj)

        return l_gastos

    raise('nao foi possivel abrir arquivo de gastos')


def save_gastos(l_gastos):
    l_gastos_raw = []

    for gasto in l_gastos:
        l_gastos_raw.append(gasto.to_dict())

    l_gastos.sort(key=lambda g: g.date)

    with open('gastos.json', 'w') as f_gastos:
        json.dump(l_gastos_raw, f_gastos, sort_keys=True, indent=4)


def print_gastos(l_gastos):
    pt = PrettyTable(['date', 'pais', 'conta', 'moeda', 'valor', 'descricao', 'categoria'])
    pt.align['valor'] = 'r'

    for g in l_gastos:
        pt.add_row([g.date, g.pais, g.conta, g.moeda, float_format(g.valor), g.descricao, g.categoria])
        #print(f'{g.date};{g.pais};{g.conta};{g.moeda};{g.valor};{g.descricao};{g.categoria};{g.periodo_de};{g.periodo_ate}')

    print(pt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Controle financeiro da viagem.')
    parser.add_argument('--transf', action='store_true', help='nova transferencia')
    parser.add_argument('--transfs', action='store_true', help='listar transferencias')
    parser.add_argument('--conta', action='store_true', help='nova conta')
    parser.add_argument('--contas', action='store_true', help='listar contas')
    parser.add_argument('--gasto', action='store_true', help='novo gasto')
    parser.add_argument('--gastos', action='store_true', help='listar gastos')
    parser.add_argument('--saldo', type=str, nargs='*', help='listar saldo')
    args = parser.parse_args()

    if args.transf:
        transferencias = load_transferencias()
        ntransf = new_transferencia()
        transferencias.append(ntransf)
        save_transferencias(transferencias)

    elif args.transfs:
        transferencias = load_transferencias()
        print_transferencias(transferencias)

    elif args.conta:
        contas = load_contas()
        nconta = new_conta()
        contas.append(nconta)
        save_contas(contas)

    elif args.contas:
        contas = load_contas()
        print_contas(contas)

    elif args.gasto:
        gastos = load_gastos()
        ngasto, ntransf = new_gasto()
        gastos.append(ngasto)
        save_gastos(gastos)

        if ntransf:
            transferencias = load_transferencias()
            transferencias.append(ntransf)
            save_transferencias(transferencias)


    elif args.gastos:
        gastos = load_gastos()
        print_gastos(gastos)

    elif args.saldo is not None:
        details = False
        all_contas = {conta.nome: conta.moeda for conta in load_contas()}

        if len(args.saldo) == 0:
            contas = [conta.nome for conta in load_contas()]
        elif len(args.saldo) == 1:
            details = True
            contas = args.saldo
        else:
            contas = args.saldo
            
        for conta in contas:
            transferencias = load_transferencias()
            saldo_transferencias = 0.0

            log_transferencias = []

            for transf in transferencias:
                added = False

                if transf.gasto:
                    continue

                if transf.from_acc == conta:
                    added = True
                    saldo_transferencias += transf.value_from

                if transf.to_acc == conta:
                    added = True
                    saldo_transferencias += transf.value_to

                if added:
                    log_transferencias.append(transf)

            log_gastos = []

            moeda = all_contas[conta]
            saldo_gastos = 0.0
            gastos = load_gastos()
            for gasto in gastos:
                if gasto.conta == conta:
                    saldo_gastos += gasto.valor
                    log_gastos.append(gasto)

            if log_transferencias:
                if details:
                    print_transferencias(log_transferencias)

                print(f'saldo transferencias {float_format(saldo_transferencias)}\n')

            if log_gastos:
                if details:
                    print_gastos(log_gastos)

                print(f'saldo gastos {float_format(saldo_gastos)}')

            saldo = saldo_transferencias + saldo_gastos
            print(f'saldo para {conta} eh de: {float_format(saldo)}')


# import json


# with open('data.txt') as finput:
#     data = json.load(finput)


# def csv_to_gasto(row):
#     fields = row.split(';') 
#     gasto = Gasto()
#     gasto.pais = fields[0] 
#     gasto.data =  fields[1]
#     gasto.origem = fields[2]
#     gasto.moeda = fields[3]
#     gasto.valor = fields[4]
#     gasto.descricao = fields[5]
#     gasto.categoria = fields[6]
#     gasto.periodo = fields[7]


# def csv_transferencia(row):
#     fields = row.split(';') 
#     transferencia = Transferencia()
#     transferencia.data = fields[0] 
#     transferencia.origem = fields[1]
#     transferencia.destino = fields[2]
#     transferencia.valor_origem = fields[3]
#     transferencia.valor_destino = fields[4]
#     transferencia.gasto = fields[5]




# TRANSFERENCIAS


# 2019-11-20;Hugo BRL;THB;-278.24;1782.16;
# 2020-01-06;Hugo BRL;USD;-6,375.00;1,500.00;
# 2020-01-20;Renata BRL;USD;-8,380.00;;2000.00;
# 2020-01-20;Renata BRL;EUR;-929.82;200.00;
# 2020-01-24;Hugo BRL;USD-;100.00;2,881.00;



# GASTOS
# Brasil;2019-09-06;Hugo BRL;BRL;-2,973.67;Passagens GRU - BKK;Nubank Credit;locomoção;;
# Tailandia;2019-11-20;Hugo BRL;THB;-1782.16;Reserva Hostel Bed Station 24/01 - 28/01;hospedagem;2020-01-24 2020-01-28;
# Brasil;2019-11-21;Hugo BRL;BRL;-178.00;Reserva de assentos - SP até Madrid;Nubank Credit;locomoção;;



# 2020-01-24;;Jantar;;;;;;-577.00;refeição
# 2020-01-24;;Sorvete;;;;;;-80.00;comida
# 2020-01-24;;Mercado;;;;;;-28.00;comida
# 2020-01-24;;Tuk tuk buda de ouro;;;;;;-20.00;transporte
# 2020-01-24;;Buda de ouro;;;;;;-80.00;ticket
# 2020-01-24;;Cerveja hostel;;;;;;-120.00;cerveja
# 2020-01-24;;Sorvete;;;;;;-80.00;comida
# 2020-01-24;;Água Hostel;;;;;;-20.00;comida
# 2020-01-24;;Transporte para Hostel;;;;;;-120.00;transporte
# 2020-01-25;Hugo;Exchange;C6 Global;-2,086.35;;500.00;;;exchange
# 2020-01-25;Hugo;Exchange;Espécie;;;-200.00;;6,032.00;exchange
# 2020-01-25;Hugo;Saque ATM;Nubank credit;-184.82;;;;1,000.00;exchange
# 2020-01-25;Hugo;Jantar;Nubank credit;-144.53;;;;954.00;refeição


