class Basket():
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if skey not in request.session:
            basket = self.session['skey'] = { }

        self.basket = basket
        

