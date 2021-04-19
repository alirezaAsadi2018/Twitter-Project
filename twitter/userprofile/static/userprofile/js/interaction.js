var retweetBtns = document.getElementsByClassName('interaction')

for (var i = 0; i < retweetBtns.length; i++) {
    retweetBtns[i].addEventListener('click', function () {
        var itemId = this.dataset.item
        var action = this.dataset.action
        console.log('itemId:', itemId, 'action:', action)

        console.log('USER:', user)
        if (user === 'AnonymousUser') {
            $('body').toast({
                class: 'error',
                message: `Please Log into your account!`
            });
            addCookieItem(itemId, action)
        } else {
            intraction(itemId, action)
        }
    })
}


function intraction(itemId, action) {
    console.log('Using is loged in, sending data..')

    var url = '/interaction/'

    fetch(url, {
        method: 'POST',
        headers: {
            'content-Type': 'application/json',
            'X-CSRFToken': csrftoken

        },
        body: JSON.stringify({'itemId': itemId, 'action': action})
    })

        .then((response) =>{
            return response.json()
        })

        .then((data) =>{
            console.log('data:', data)
            location.reload()
        })

}
