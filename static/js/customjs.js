
const host = "http://127.0.0.1:8000/"


const showLoader = () => {
    document.querySelector('.loading-bar').style.display = "grid";
}


//showLoader();




const notify = (message, status, position, gravity) => {
    const backgrounds = {
        success: "#38cc9b",
        error: "#ff7782",
        primary: "#fd7016",
    }

    
    Toastify({
        text: message,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: gravity || "top", // `top` or `bottom`
        position: position || "center", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background:backgrounds[status] || "#fd7016",
            backgroundColor: backgrounds[status] || "#fd7016",
            color: "ffffff",
        },
        onClick: function(){} // Callback after click
        }).showToast();
}



var filter_select = document.getElementById("order-select")

if (filter_select) {
    filter_select.addEventListener('change', (event) => {
    console.log(event.target.value)
    var page = document.querySelector("#pageNo").innerHTML
    var search = document.querySelector("#search_phrase").innerHTML
    showLoader();
    window.location.href=`${host}search?&searchphrase=${search}&page=${page}&order=${event.target.value}`
})
}


function checkAwaitingWish() {
    const user = JSON.parse(document.getElementById('user_req_id').textContent)
    if (user) {
        const wish = localStorage.getItem('awaiting_wish')
        if (wish) {
            localStorage.removeItem('awaiting_wish')
            addToWishList(wish);
        }
    }
}



function getShoppingCartItems() {
    var cart = JSON.parse(localStorage.getItem("shoppingCart")) || []
    var cartbox = document.querySelector('.minicart-product-list')
    if (cart) {
        cartbox.innerHTML = '';
        var cart_total = 0;
        for (let x = 0; x < cart.length; x++){
            var data = cart[x];
            cartbox.innerHTML += `
             <li>
                <a href="${host}${data.category_slug}/${data.product_slug}" class="minicart-product-image">
                    <img src="${data.image}" alt="cart products">
                </a>
                <div class="minicart-product-details">
                    <h6><a href="single-product.html">${data.name}</a></h6>
                    <span>₦${data.price.toLocaleString("en-US")} x ${data.quantity}</span>
                </div>
                <button class="close" title="Remove" onclick="deleteItemFromCart('${data.uid}')">
                    <i class="fa fa-close"></i>
                </button>
            </li>
            `
            cart_total += (data.price * data.quantity)
        }

        document.getElementById('cart_total').innerHTML = "₦" + cart_total.toLocaleString("en-US")
        document.querySelector('.hm-minicart-trigger').innerHTML = `
            <span class="item-icon"></span>
            <span class="item-text">₦${cart_total.toLocaleString("en-US")}
                <span class="cart-item-count">${cart.length}</span>
            </span>
        
        
        `
    }
    
}

checkAwaitingWish();
getShoppingCartItems();





function addToCart(uid, name, price, quantity, image, category_slug, product_slug) {
    
    if (quantity && name && uid && price && category_slug && product_slug) {
        function updateCart(uid) {
            var cart = JSON.parse(localStorage.getItem("shoppingCart")) || []
            for (let x = 0; x < cart.length; x++){
                data = cart[x]
                if (data.uid === uid) {
                    data.quantity = data.quantity + quantity
                    data.item_total = data.price * data.quantity
                    localStorage.setItem('shoppingCart', JSON.stringify(cart));
                    return true
                }
            }
            return false;
        }


    if (updateCart(uid)) {
        if (screen.width <= 600) {
            notify(
                "Cart was Updated Successfully",
                "success",
                "center",
                "bottom"
            )
        } else {
            notify(
                "Cart was Updated Successfully",
                "success",
                "center",
                "top"
            )
        }
    }
    else {
        var cart = JSON.parse(localStorage.getItem("shoppingCart")) || []
        var price_int =  parseInt(price.replace(',', ''))
        cart.push({
            uid: uid,
            name: name,
            image: image,
            quantity: quantity,
            price: price_int,
            item_total:price_int,
        })

        localStorage.setItem('shoppingCart', JSON.stringify(cart));
         if (screen.width <= 600) {
            notify(
                "Item has been added to Cart",
                "success",
                "center",
                "bottom"
            )
        } else {
            notify(
                "Item has been added to Cart",
                "success",
                "center",
                "top"
            )
        }

    }
    getShoppingCartItems();

    }
}



function deleteItemFromCart(uid) {
    function deleteFromCartFunc(uid) {
        var cart = JSON.parse(localStorage.getItem("shoppingCart")) || []
        for (let x = 0; x < cart.length; x++){
            data = cart[x]
            if (data.uid === uid) {
                cart.splice(x, 1)
                localStorage.setItem('shoppingCart', JSON.stringify(cart));
                return true
            }
        }
        return false;
    }

    if (deleteFromCartFunc(uid)) {
         if (screen.width <= 600) {
            notify(
                "Item was removed from cart.",
                "success",
                "center",
                "bottom"
            )
        } else {
            notify(
                "Item was removed from cart.",
                "success",
                "center",
                "top"
            )
        }
        getShoppingCartItems();

    }

}


function peek(name, category, price, img_list, uid, desc, colored, blank, is_in_stock) {

    
    var title = name;
    var category = category || '';
    var price = price || '';
    var description = desc
    var img_list = img_list.split(',');
    var colored = colored || 0;
    var blank = blank || 5;
    var is_in_stock = is_in_stock
    var uid = uid
    
    function get_Large_Imgs(list) {
        var l_imgdiv = ``   
        for (let x = 0; x < list.length; x++){
            l_imgdiv += `
                 <div class="lg-image">
                                <img src="${list[x]}" alt="product image">
                </div>
            `
        }
        return l_imgdiv
    }
    function get_Small_Imgs(list) {
        var l_imgdiv = ``   
        for (let x = 0; x < list.length; x++){
            l_imgdiv += `
                 <div class="sm-image"><img src="${list[x]}" alt="product image thumb" style="width:150px;"></div>
            `
        }
        return l_imgdiv
    }
    
    function getStars(colored, blank) {
       
        var starbox = ``
        for (let x = 0; x < colored; x++){
            starbox += `
            <li><i class="fa fa-star-o"></i></li>
               `
        }
        for (let x = 0; x < blank; x++){
            starbox += `
            <li class="no-star"><i class="fa fa-star-o"></i></li>
               `
        }
        return starbox
    }

    function checkStock(stock) {
        
        if (`${stock}`.toLowerCase() === 'true') {
            return `
             <div class="single-add-to-cart">
                                <form action="#" class="cart-quantity">
                                    
                                    <button class="add-to-cart" type="button" onclick="addToCart('${uid}','${title}', '${price}',1, '${img_list[0]}');">Add to cart</button>
                                </form>
                            </div>
                            <div class="product-additional-info pt-25">
                                <span class="wishlist-btn" onclick="addToWishList('${uid}')"><i class="fa fa-heart-o"></i>Add to wishlist</a>
                                <div class="product-social-sharing pt-25">
                                    <ul>
                                        <li class="facebook"><a href="#"><i class="fa fa-facebook"></i>Facebook</a></li>
                                        <li class="twitter"><a href="#"><i class="fa fa-twitter"></i>Twitter</a></li>
                                        <li class="google-plus"><a href="#"><i class="fa fa-google-plus"></i>Google +</a></li>
                                        <li class="instagram"><a href="#"><i class="fa fa-instagram"></i>Instagram</a></li>
                                    </ul>
                                </div>
                            </div>
            
            
            `
        }
        return `
         <div class="single-add-to-cart">
                                <form action="#" class="cart-quantity">          
                                    <button class="add-to-cart out-of-stock" type="button" style="cursor:default;">Out of Stock</button>
                                </form>
                            </div>
                            <div class="product-additional-info pt-25">
                                
                            </div>
        
        `
    }


    var modal_content = document.querySelector(".modal-content")
    
    modal_content.innerHTML = `
         <div class="modal-body">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-huidden="true">&times;</span>
            </button>
            <div class="modal-inner-area row">
                <div class="col-lg-5 col-md-6 col-sm-6">
                    <!-- Product Details Left -->
                    <div class="product-details-left">
                    <div class="product-details-images sluider-navigation-1">
                             ${get_Large_Imgs(img_list)}
                           
                    </div>
                    <div class="product-details-thumbs sluider-thumbs-1">                                        
                            ${get_Small_Imgs(img_list)}
                         
                    </div>
                       
                    </div>
                    <!--// Product Details Left -->
                </div>

                <div class="col-lg-7 col-md-6 col-sm-6">
                    <div class="product-details-view-content pt-60">
                        <div class="product-info">
                            <h2>${title}</h2>
                            <span class="product-details-ref">${category}</span>
                            <div class="rating-box pt-20">
                                <ul class="rating rating-with-review-item">
                                    
                                    ${getStars(colored, blank)}
                                </ul>
                            </div>
                            <div class="price-box pt-20">
                                <span class="new-price new-price-2">₦${price}</span>
                            </div>
                            <div class="product-desc">
                                <p>
                                    <span>${description}</span>
                                </p>
                            </div>

                            ${checkStock(is_in_stock)}
                            
                           
                        </div>
                    </div>
                </div>
            </div>
        </div>

    
    `
}




function addToWishList(uid) {
    const user = JSON.parse(document.getElementById('user_req_id').textContent)
    
    function getCSRFToken() {
        const csrfCookie = document.cookie.split('; ').find(cookie => cookie.startsWith('csrftoken='));
        if (csrfCookie) {
            return csrfCookie.split('=')[1];
        }
        return null;
    }

    if (user) {
        const csrftoken = getCSRFToken()

    fetch(host + 'wishlist/add', {
        method: "POST",
        body: JSON.stringify({
            user_id:user,
            uid:uid
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "X-CSRFToken": csrftoken,
        }
        
    })
        .then(response => { 
            if (!response.ok) {
                if (screen.width <= 600) {
                        notify(
                            "Error: Please check your Internet connection and try again",
                            "error",
                            "center",
                            "bottom"
                        )
                    } else {
                        notify(
                            "Error: Please check your Internet connection and try again",
                            "error",
                            "center",
                            "top"
                        )
                    }
                throw new Error('Network response was not ok');
                 
            }
            return response.json()
        })
        .then(data => {
            
            if (data.message === 'successful') {
                 if (screen.width <= 600) {
                        notify(
                            "Item has been added to wishlist",
                            "success",
                            "center",
                            "bottom"
                        )
                    } else {
                        notify(
                            "Item has been added to wishlist",
                            "success",
                            "center",
                            "top"
                        )
                    }
                var count = document.getElementById('wishlist_count');
                count.innerHTML = parseInt(count.innerHTML) + 1;
            }
            console.log(data)
        })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        if (screen.width <= 600) {
                        notify(
                            "Error: There was a problem with the Action. Please try agin later",
                            "error",
                            "center",
                            "bottom"
                        )
                    } else {
                        notify(
                            "Error: There was a problem with the Action. Please try agin later",
                            "error",
                            "center",
                            "top"
                        )
                    }
    });

    } else {
        localStorage.setItem('awaiting_wish', uid)
        if (screen.width <= 600) {
                    notify(
                        "Login to add this Item",
                        "primary",
                        "center",
                        "bottom"
                    )
                } else {
                    notify(
                        "Login to add this Item",
                        "primary",
                        "center",
                        "top"
                    )
                }
                
        window.location.href = host + 'wishlist';
    }
    
}


function removeFromWishList(uid) {
    const user = JSON.parse(document.getElementById('user_req_id').textContent)
    
    function getCSRFToken() {
        const csrfCookie = document.cookie.split('; ').find(cookie => cookie.startsWith('csrftoken='));
        if (csrfCookie) {
            return csrfCookie.split('=')[1];
        }
        return null;
    }

    if (user) {
        const csrftoken = getCSRFToken()

    fetch(host + 'wishlist/remove', {
        method: "POST",
        body: JSON.stringify({
            user_id:user,
            uid:uid
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "X-CSRFToken": csrftoken,
        }
        
    })
        .then(response => { 
            if (!response.ok) {
                if (screen.width <= 600) {
                        notify(
                            "Error: Please check your Internet connection and try again",
                            "error",
                            "center",
                            "bottom"
                        )
                    } else {
                        notify(
                            "Error: Please check your Internet connection and try again",
                            "error",
                            "center",
                            "top"
                        )
                    }
                throw new Error('Network response was not ok');
            }
            return response.json()
        })
        .then(data => {
            
            if (data.message === 'successful') {
                if (screen.width <= 600) {
                        notify(
                            "Item has been removed from your Wishlist",
                            "success",
                            "center",
                            "bottom"
                        )
                    } else {
                        notify(
                            "Item has been removed from your Wishlist",
                            "success",
                            "center",
                            "top"
                        )
                    }
                var count = document.getElementById('wishlist_count');
                count.innerHTML = parseInt(count.innerHTML) - 1;
                document.getElementById(`wishlist_${uid}`).remove();
            }
            console.log(data)
        })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
         if (screen.width <= 600) {
                        notify(
                            "Error: There was a problem with the Action. Please try agin later",
                            "error",
                            "center",
                            "bottom"
                        )
                    } else {
                        notify(
                            "Error: There was a problem with the Action. Please try agin later",
                            "error",
                            "center",
                            "top"
                        )
                    }
    });
    }
    
}




var pass1 = document.querySelector('#pass1')
var pass2 = document.querySelector('#pass2')
var reg_button = document.querySelector('#reg-button')



if(pass1){
    pass1.addEventListener('input', () => {
        if (pass1.value === pass2.value && pass1.value.trim != "" && pass1.value.length>=8) {
            reg_button.style.opacity="";
            reg_button.disabled = false;
            pass1.style.border = "";
        } else {
            reg_button.style.opacity=0.5;
            reg_button.disabled = true;
            pass1.style.border = "2px solid #e32";
        }
    })

}

if (pass2){
    pass2.addEventListener('input', () => {
    if (pass1.value === pass2.value && pass1.value.trim != "" && pass1.value.length>=8) {
        reg_button.style.opacity="";
        reg_button.disabled = false;
        pass1.style.border = "";
    } else {
        reg_button.style.opacity=0.5;
        reg_button.disabled = true;
        
    }
})
}



if(document.readyState === "complete") {
    // Fully loaded!
}
else if(document.readyState === "interactive") {
    // DOM ready! Images, frames, and other subresources are still downloading.
}
else {
    // Loading still in progress.
    // To wait for it to complete, add "DOMContentLoaded" or "load" listeners.

    window.addEventListener("DOMContentLoaded", () => {
        // DOM ready! Images, frames, and other subresources are still downloading.
    });

    window.addEventListener("load", () => {
        // Fully loaded!
        document.querySelector('.loading-bar').style.display = 'none';
    });
}