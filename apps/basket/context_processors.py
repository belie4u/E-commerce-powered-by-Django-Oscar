from .forms import BasketCurrencyForm


def currency_form (request):
    """
    Context proccessor to provide a currency selection from throught the sit 
    Initialises ` currenc_form` with GET or POST data
    """

    if request.method == 'POST':
        form = BasketCurrencyForm(request.POST)
    
    else:
        form = BasketCurrencyForm(request.GET)
    
    return {'currency_form':form}