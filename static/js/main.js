// // ========== سبد خرید ==========
// function getCart() {
//     return JSON.parse(localStorage.getItem('cart')) || [];
// }
//
// function saveCart(cart) {
//     localStorage.setItem('cart', JSON.stringify(cart));
// }
//
// function addToCart(productId, productName, productPrice, productImg) {
//     let cart = getCart();
//     cart.push({
//         id: parseInt(productId),
//         name: productName,
//         price: parseInt(productPrice),
//         img: productImg
//     });
//     saveCart(cart);
//     updateCartCount();
//     showNotification(productName + " به سبد خرید اضافه شد 🌹");
// }
//
// function removeFromCart(index) {
//     let cart = getCart();
//     cart.splice(index, 1);
//     saveCart(cart);
//     updateCartCount();
//     if (window.location.pathname.includes('cart.html')) {
//         displayCartItems();
//     }
// }
//
// function updateCartCount() {
//     const cart = getCart();
//     const cartCountSpans = document.querySelectorAll('#cartCountNav');
//     cartCountSpans.forEach(function (span) {
//         if (span) span.innerText = cart.length;
//     });
// }
//
// function displayCartItems() {
//     const cart = getCart();
//     const cartContainer = document.getElementById('cartItems');
//     const totalContainer = document.getElementById('cartTotal');
//
//     if (!cartContainer) return;
//
//     if (cart.length === 0) {
//         cartContainer.innerHTML = '<div class="empty-cart">🛒 سبد خرید شما خالی است</div>';
//         if (totalContainer) totalContainer.innerHTML = '';
//         return;
//     }
//
//     let cartHtml = '';
//     for (let i = 0; i < cart.length; i++) {
//         cartHtml += `
//             <div class="cart-item">
//                 <div class="cart-item-info">
//                     <span class="cart-item-emoji">${cart[i].img}</span>
//                     <div>
//                         <div class="cart-item-name">${cart[i].name}</div>
//                         <div class="cart-item-price">${cart[i].price.toLocaleString()} تومان</div>
//                     </div>
//                 </div>
//                 <button class="remove-from-cart" data-index="${i}">❌</button>
//             </div>
//         `;
//     }
//     cartContainer.innerHTML = cartHtml;
//
//     let total = 0;
//     for (let i = 0; i < cart.length; i++) {
//         total += cart[i].price;
//     }
//     if (totalContainer) {
//         totalContainer.innerHTML = '<div class="cart-total">مجموع: ' + total.toLocaleString() + ' تومان</div>';
//     }
//
//     const removeBtns = document.querySelectorAll('.remove-from-cart');
//     for (let i = 0; i < removeBtns.length; i++) {
//         removeBtns[i].addEventListener('click', function (e) {
//             const index = parseInt(this.dataset.index);
//             removeFromCart(index);
//         });
//     }
// }

function showNotification(message) {
    const notif = document.createElement('div');
    notif.className = 'notification';
    notif.textContent = message;
    notif.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: #4a2c22;
        color: white;
        padding: 12px 24px;
        border-radius: 50px;
        z-index: 1000;
        font-size: 14px;
        white-space: nowrap;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        font-family: 'Estedad', sans-serif;
    `;
    document.body.appendChild(notif);
    setTimeout(function () {
        notif.remove();
    }, 2500);
}

// function searchProducts(query) {
//     const products = document.querySelectorAll('.product-card');
//     if (!query.trim()) {
//         for (let i = 0; i < products.length; i++) {
//             products[i].style.display = '';
//         }
//         return;
//     }
//
//     for (let i = 0; i < products.length; i++) {
//         const title = products[i].querySelector('h3');
//         const desc = products[i].querySelector('p');
//         const titleText = title ? title.innerText : '';
//         const descText = desc ? desc.innerText : '';
//         if (titleText.includes(query) || descText.includes(query)) {
//             products[i].style.display = '';
//         } else {
//             products[i].style.display = 'none';
//         }
//     }
// }

function initProductDetail() {
    const decreaseBtns = document.querySelectorAll('.qty-decrease');
    const increaseBtns = document.querySelectorAll('.qty-increase');
    const quantityInputs = document.querySelectorAll('.product-quantity');

    for (let i = 0; i < decreaseBtns.length; i++) {
        decreaseBtns[i].addEventListener('click', function () {
            let current = parseInt(quantityInputs[i].value);
            if (current > 1) {
                quantityInputs[i].value = current - 1;
            }
        });
    }

    for (let i = 0; i < increaseBtns.length; i++) {
        increaseBtns[i].addEventListener('click', function () {
            let current = parseInt(quantityInputs[i].value);
            if (current < 99) {
                quantityInputs[i].value = current + 1;
            }
        });
    }

    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    for (let i = 0; i < tabBtns.length; i++) {
        tabBtns[i].addEventListener('click', function () {
            const tabId = this.dataset.tab;

            for (let j = 0; j < tabBtns.length; j++) {
                tabBtns[j].classList.remove('active');
            }
            for (let j = 0; j < tabPanes.length; j++) {
                tabPanes[j].classList.remove('active');
            }

            this.classList.add('active');
            const activePane = document.getElementById(tabId);
            if (activePane) {
                activePane.classList.add('active');
            }
        });
    }

    const ratingStars = document.querySelectorAll('.rating-stars span');
    let selectedRating = 0;

    for (let i = 0; i < ratingStars.length; i++) {
        ratingStars[i].addEventListener('click', function () {
            selectedRating = parseInt(this.dataset.rating);
            for (let j = 0; j < ratingStars.length; j++) {
                if (j < selectedRating) {
                    ratingStars[j].textContent = '★';
                    ratingStars[j].classList.add('active');
                } else {
                    ratingStars[j].textContent = '☆';
                    ratingStars[j].classList.remove('active');
                }
            }
        });
    }

    const submitComment = document.getElementById('submitComment');
    if (submitComment) {
        submitComment.addEventListener('click', function () {
            const commentText = document.getElementById('newComment').value;
            if (!commentText.trim()) {
                showNotification('لطفاً نظر خود را بنویسید');
                return;
            }

            const commentsList = document.getElementById('commentsList');
            const newComment = document.createElement('div');
            newComment.className = 'comment-item';
            let starRating = '';
            for (let i = 0; i < (selectedRating || 5); i++) starRating += '★';
            for (let i = 0; i < (5 - (selectedRating || 5)); i++) starRating += '☆';
            newComment.innerHTML = `
                <div class="comment-header">
                    <strong>شما</strong>
                    <span class="comment-date">${new Date().toLocaleDateString('fa-IR')}</span>
                    <div class="comment-rating">${starRating}</div>
                </div>
                <div class="comment-text">${commentText}</div>
            `;

            commentsList.insertBefore(newComment, commentsList.firstChild);
            document.getElementById('newComment').value = '';

            for (let i = 0; i < ratingStars.length; i++) {
                ratingStars[i].textContent = '☆';
                ratingStars[i].classList.remove('active');
            }
            selectedRating = 0;

            showNotification('نظر شما با موفقیت ثبت شد 🌹');
        });
    }
}

// function updateCheckoutTotal() {
//     const cart = getCart();
//     let subtotal = 0;
//     for (let i = 0; i < cart.length; i++) {
//         subtotal += cart[i].price;
//     }
//     const shipping = 35000;
//     const grandTotal = subtotal + shipping;
//
//     const subtotalEl = document.getElementById('cartSubtotal');
//     const grandTotalEl = document.getElementById('cartGrandTotal');
//
//     if (subtotalEl) subtotalEl.innerText = subtotal.toLocaleString() + ' تومان';
//     if (grandTotalEl) grandTotalEl.innerText = grandTotal.toLocaleString() + ' تومان';
// }
//
// document.addEventListener('DOMContentLoaded', function () {
//     updateCartCount();
//
//     const navToggle = document.getElementById('navToggle');
//     const navMenu = document.getElementById('navMenu');
//     if (navToggle && navMenu) {
//         navToggle.addEventListener('click', function () {
//             navMenu.classList.toggle('active');
//         });
//     }
//
//     const cartBadge = document.getElementById('cartBadge');
//     if (cartBadge) {
//         cartBadge.addEventListener('click', function () {
//             window.location.href = 'cart.html';
//         });
//     }
//
//     const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
//     for (let i = 0; i < addToCartBtns.length; i++) {
//         addToCartBtns[i].addEventListener('click', function (e) {
//             e.stopPropagation();
//             const id = this.dataset.id;
//             const name = this.dataset.name;
//             const price = this.dataset.price;
//             const img = this.dataset.img;
//             addToCart(id, name, price, img);
//         });
//     }
//
//     const detailBtn = document.getElementById('detailAddToCart');
//     if (detailBtn) {
//         detailBtn.addEventListener('click', function () {
//             const id = this.dataset.id;
//             const name = this.dataset.name;
//             const price = this.dataset.price;
//             const img = this.dataset.img;
//             addToCart(id, name, price, img);
//         });
//     }
//
//     const searchInput = document.getElementById('searchInput');
//     if (searchInput) {
//         searchInput.addEventListener('input', function (e) {
//             searchProducts(e.target.value);
//         });
//     }
//
//     if (document.getElementById('cartItems')) {
//         displayCartItems();
//     }
//
//     if (document.querySelector('.product-detail-wrapper')) {
//         initProductDetail();
//     }
//
//     if (document.getElementById('cartSubtotal')) {
//         updateCheckoutTotal();
//     }
//
//     const paymentMethods = document.querySelectorAll('.payment-method');
//     for (let i = 0; i < paymentMethods.length; i++) {
//         paymentMethods[i].addEventListener('click', function () {
//             for (let j = 0; j < paymentMethods.length; j++) {
//                 paymentMethods[j].classList.remove('selected');
//             }
//             this.classList.add('selected');
//         });
//     }
//
//     const authTabs = document.querySelectorAll('.auth-tab');
//     const authForms = document.querySelectorAll('.auth-form');
//     for (let i = 0; i < authTabs.length; i++) {
//         authTabs[i].addEventListener('click', function () {
//             const tabId = this.dataset.tab;
//             for (let j = 0; j < authTabs.length; j++) {
//                 authTabs[j].classList.remove('active');
//             }
//             for (let j = 0; j < authForms.length; j++) {
//                 authForms[j].classList.remove('active');
//             }
//             this.classList.add('active');
//             const activeForm = document.getElementById(tabId + '-form');
//             if (activeForm) {
//                 activeForm.classList.add('active');
//             }
//         });
//     }
//
//     const productCards = document.querySelectorAll('.product-card');
//     for (let i = 0; i < productCards.length; i++) {
//         productCards[i].addEventListener('click', function (e) {
//             if (!e.target.classList.contains('add-to-cart-btn') &&
//                 !e.target.classList.contains('qty-btn') &&
//                 !e.target.classList.contains('product-quantity')) {
//                 const productId = this.dataset.productId;
//                 if (productId) {
//                     window.location.href = 'product-detail.html?id=' + productId;
//                 }
//             }
//         });
//     }
//
//     const checkoutBtn = document.querySelector('.checkout-form .btn');
//     if (checkoutBtn) {
//         checkoutBtn.addEventListener('click', function () {
//             alert('سفارش شما با موفقیت ثبت شد! ممنون از خرید شما از گلابو 🌹');
//         });
//     }
//
//     // ====== فیلتر مقالات ======
//     initBlogFilters();
//
//     // ====== ثبت نظر در مقاله ======
//     initBlogComment();
//
//     if (document.querySelector('.profile-container')) {
//         initProfile();
//     }
// });

// ========== اسکرول محصولات با فلش ==========
function initProductScroll() {
    const scrollContainer = document.getElementById('productsScroll');
    const scrollLeftBtn = document.getElementById('scrollLeft');
    const scrollRightBtn = document.getElementById('scrollRight');

    if (!scrollContainer) return;

    // اسکرول با فلش چپ
    if (scrollLeftBtn) {
        scrollLeftBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            const scrollAmount = scrollContainer.querySelector('.product-card')?.offsetWidth || 220;
            scrollContainer.scrollBy({
                left: -(scrollAmount + 20),
                behavior: 'smooth'
            });
        });
    }

    // اسکرول با فلش راست
    if (scrollRightBtn) {
        scrollRightBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            const scrollAmount = scrollContainer.querySelector('.product-card')?.offsetWidth || 220;
            scrollContainer.scrollBy({
                left: scrollAmount + 20,
                behavior: 'smooth'
            });
        });
    }

    // اسکرول با موس (ویل)
    scrollContainer.addEventListener('wheel', function (e) {
        if (e.deltaX !== 0) {
            e.preventDefault();
            scrollContainer.scrollBy({
                left: e.deltaX,
                behavior: 'smooth'
            });
        }
    }, {passive: false});
}

// فراخوانی در DOMContentLoaded
// این خط را به تابع DOMContentLoaded اضافه کن:
// initProductScroll();

function initBlogFilters() {
    const catBtns = document.querySelectorAll('.blog-cat-btn');
    const blogCards = document.querySelectorAll('.blog-card');

    if (!catBtns.length || !blogCards.length) return;

    catBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            catBtns.forEach(function (b) {
                b.classList.remove('active');
            });
            this.classList.add('active');

            const category = this.dataset.cat;

            blogCards.forEach(function (card) {
                if (category === 'all' || card.dataset.category === category) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

// ========== ثبت نظر در صفحه جزئیات مقاله ==========
function initBlogComment() {
    const submitComment = document.getElementById('submitBlogComment');
    if (!submitComment) return;

    submitComment.addEventListener('click', function () {
        const commentText = document.getElementById('blogComment').value;
        if (!commentText.trim()) {
            showNotification('لطفاً نظر خود را بنویسید');
            return;
        }

        const commentsSection = document.querySelector('.blog-comments-section');
        const addCommentForm = document.querySelector('.blog-add-comment');

        if (!commentsSection || !addCommentForm) return;

        const newComment = document.createElement('div');
        newComment.className = 'blog-comment';
        newComment.innerHTML = `
            <div class="comment-avatar">👤</div>
            <div class="comment-body">
                <div class="comment-header">
                    <strong>شما</strong>
                    <span class="comment-date">${new Date().toLocaleDateString('fa-IR')}</span>
                </div>
                <p>${commentText}</p>
            </div>
        `;

        commentsSection.insertBefore(newComment, addCommentForm);
        document.getElementById('blogComment').value = '';
        showNotification('نظر شما با موفقیت ثبت شد 🌹');
    });
}

// ========== توابع صفحه پروفایل ==========
// function initProfile() {
//     // ====== تب‌ها ======
//     const profileTabs = document.querySelectorAll('.profile-tab');
//     const tabContents = document.querySelectorAll('.profile-tab-content');
//
//     profileTabs.forEach(function (tab) {
//         tab.addEventListener('click', function () {
//             const tabId = this.dataset.tab;
//
//             profileTabs.forEach(function (t) {
//                 t.classList.remove('active');
//             });
//             tabContents.forEach(function (c) {
//                 c.classList.remove('active');
//             });
//
//             this.classList.add('active');
//             const activeContent = document.getElementById('tab-' + tabId);
//             if (activeContent) {
//                 activeContent.classList.add('active');
//             }
//         });
//     });
//
//     // ====== آپلود عکس پروفایل ======
//     const avatarUpload = document.getElementById('avatarUpload');
//     const avatarPlaceholder = document.querySelector('.profile-avatar .avatar-placeholder');
//
//     if (avatarUpload && avatarPlaceholder) {
//         avatarUpload.addEventListener('change', function (e) {
//             const file = this.files[0];
//             if (file) {
//                 const reader = new FileReader();
//                 reader.onload = function (event) {
//                     avatarPlaceholder.style.backgroundImage = 'url(' + event.target.result + ')';
//                     avatarPlaceholder.style.backgroundSize = 'cover';
//                     avatarPlaceholder.style.backgroundPosition = 'center';
//                     avatarPlaceholder.textContent = '';
//                     showProfileSuccess('عکس پروفایل با موفقیت آپلود شد 🌹');
//                 };
//                 reader.readAsDataURL(file);
//             }
//         });
//     }
//
//     // ====== ذخیره اطلاعات شخصی ======
//     const saveInfoBtn = document.getElementById('saveInfoBtn');
//     if (saveInfoBtn) {
//         saveInfoBtn.addEventListener('click', function () {
//             showProfileSuccess('اطلاعات شخصی با موفقیت ذخیره شد ✅');
//             hideProfileError();
//         });
//     }
//
//     // ====== تغییر رمز عبور ======
//     const savePasswordBtn = document.getElementById('savePasswordBtn');
//     if (savePasswordBtn) {
//         savePasswordBtn.addEventListener('click', function () {
//             const inputs = document.querySelectorAll('#passwordForm input');
//             let isValid = true;
//
//             inputs.forEach(function (input) {
//                 if (!input.value.trim()) {
//                     isValid = false;
//                 }
//             });
//
//             if (!isValid) {
//                 showProfileError('لطفاً تمام فیلدها را پر کنید');
//                 return;
//             }
//
//             const newPass = inputs[1].value;
//             const confirmPass = inputs[2].value;
//
//             if (newPass !== confirmPass) {
//                 showProfileError('رمز عبور جدید و تکرار آن مطابقت ندارند');
//                 return;
//             }
//
//             if (newPass.length < 8) {
//                 showProfileError('رمز عبور باید حداقل ۸ کاراکتر باشد');
//                 return;
//             }
//
//             showProfileSuccess('رمز عبور با موفقیت تغییر کرد 🔑');
//             // hideProfileError();
//
//             inputs.forEach(function (input) {
//                 input.value = '';
//             });
//         });
//     }
//
//     // ====== ذخیره آدرس ======
//     const saveAddressBtn = document.getElementById('saveAddressBtn');
//     if (saveAddressBtn) {
//         saveAddressBtn.addEventListener('click', function () {
//             showProfileSuccess('آدرس با موفقیت ذخیره شد 📍');
//             hideProfileError();
//         });
//     }
//
//     // ====== دکمه‌های انصراف ======
//     const cancelBtns = document.querySelectorAll('#cancelInfoBtn, #cancelPasswordBtn, #cancelAddressBtn');
//     cancelBtns.forEach(function (btn) {
//         btn.addEventListener('click', function () {
//             hideProfileSuccess();
//             hideProfileError();
//             showNotification('تغییرات لغو شد');
//         });
//     });
// }
//
// // ====== نمایش پیام موفقیت ======
// function showProfileSuccess(message) {
//     const successDiv = document.getElementById('profileSuccess');
//     if (successDiv) {
//         successDiv.textContent = '✅ ' + message;
//         successDiv.classList.add('show');
//         setTimeout(function () {
//             successDiv.classList.remove('show');
//         }, 5000);
//     }
// }
//
// // ====== نمایش پیام خطا ======
// function showProfileError(message) {
//     const errorDiv = document.getElementById('profileError');
//     if (errorDiv) {
//         errorDiv.textContent = '❌ ' + message;
//         errorDiv.classList.add('show');
//     }
// }
//
// // ====== مخفی کردن پیام موفقیت ======
// function hideProfileSuccess() {
//     const successDiv = document.getElementById('profileSuccess');
//     if (successDiv) {
//         successDiv.classList.remove('show');
//     }
// }
//
// // ====== مخفی کردن پیام خطا ======
// function hideProfileError() {
//     const errorDiv = document.getElementById('profileError');
//     if (errorDiv) {
//         errorDiv.classList.remove('show');
//     }
// }

// ====== فراخوانی در DOMContentLoaded ======
// این خط رو به تابع DOMContentLoaded اضافه کن:
// initProfile();