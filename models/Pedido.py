class Pedido:
    def __init__(self, id, data, status, cliente_id, entregador_id):
        self.id = id
        self.data = data
        self.status = status
        self.cliente_id = cliente_id
        self.entregador_id = entregador_id