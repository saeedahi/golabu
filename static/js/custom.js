function addComment(articleOrProductID) {
    var comment = $('#bpComment').val();
    var parent_id = $('#parent_id').val();

    $.post('/blog/add-comment/', {
        comment: comment,
        articleOrProduct_id: articleOrProductID,
        parent_id: parent_id,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    }).then(res => {
        // console.log(res);
        $('#comments_area').html(res);
        $('#bpComment').val('');
        $('#parent_id').val('');

        if (parent_id) {
            document.getElementById('single-comment-box-' + parent_id).scrollIntoView({
                behavior: 'smooth'
            })
        } else {
            document.getElementById('comments_area').scrollIntoView({
                behavior: 'smooth'
            })
        }
    });
}

function addProductComment(productId) {
    var comment = $('#product-comment').val();
    var parent_id = $('#comment-parent-id').val();

    $.post('/products/add-comment/', {
        comment: comment,
        product_id: productId,
        parent_id: parent_id,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    }).then(res => {
        $('#commentsList').html(res);
        $('#product-comment').val('');
        $('#comment-parent-id').val('')

        if (parent_id !== null || parent_id !== '') {
            document.getElementById('commentsList').scrollIntoView({
                behavior: 'smooth'
            })
        } else {
            document.getElementById('single-comment-box-' + parent_id).scrollIntoView({
                behavior: 'smooth'
            })
        }
    })
}

function fillParentID(parentID) {
    $('#parent_id').val(parentID);
    $('#comment-parent-id').val(parentID);
    document.getElementById('comment-form').scrollIntoView({
        behavior: 'smooth'
    });
}

// function fillCommentParentID(parentID) {
//     $('#comment-parent-id').val(parentID);
//     document.getElementById('comment-form').scrollIntoView({
//          behavior: 'smooth'
//     });
// }

function likeComment(commentID, type) {
    $.post(`/${type}/like/`, {
        comment_id: commentID,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    }).then(res => {
        $('#like-count-' + commentID).text(res.count.toLocaleString('fa-IR'));
    })
}

// function setArticleCategory(categoryID) {
//     console.log(categoryID);
// }


// check password

const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirm_password");

const lengthItem = document.getElementById("length");
const upperItem = document.getElementById("uppercase");
const numberItem = document.getElementById("number");
const specialItem = document.getElementById("special");
const matchItem = document.getElementById("match");

function setState(element, valid) {
    if (valid) {
        element.classList.add("valid");
        element.innerHTML = "✅ " + element.textContent.replace(/^❌ |^✅ /, "");
    } else {
        element.classList.remove("valid");
        element.innerHTML = "❌ " + element.textContent.replace(/^❌ |^✅ /, "");
    }
}

function validatePassword() {

    const value = password.value;

    setState(lengthItem, value.length >= 8);
    setState(upperItem, /[A-Z]/.test(value));
    setState(numberItem, /\d/.test(value));
    setState(specialItem, /[!@#$%^&*]/.test(value));

    setState(matchItem,
        value.length > 0 &&
        value === confirmPassword.value
    );
}

password.addEventListener("input", validatePassword);
confirmPassword.addEventListener("input", validatePassword);


document.addEventListener("DOMContentLoaded", function () {

    const tabs = document.querySelectorAll(".profile-tab");
    const contents = document.querySelectorAll(".profile-tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", function () {

            // حذف active از همه تب‌ها
            tabs.forEach(t => t.classList.remove("active"));

            // مخفی کردن همه محتواها
            contents.forEach(content => {
                content.classList.remove("active");
            });

            // فعال کردن تب انتخاب شده
            this.classList.add("active");

            // نمایش محتوای مربوطه
            const target = document.getElementById("tab-" + this.dataset.tab);

            if (target) {
                target.classList.add("active");
            }
        });
    });

});

document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".toast").forEach(function (toast) {

        // دکمه بستن

        toast.querySelector(".toast-close").onclick = function () {

            hideToast(toast);

        };

        // بعد از ۵ ثانیه

        setTimeout(function () {

            hideToast(toast);

        }, 5000);

    });

});

function hideToast(toast) {

    toast.style.opacity = "0";

    toast.style.transform = "translateY(-30px)";

    setTimeout(function () {

        toast.remove();

    }, 400);

}


function addProductToOrder(productId) {
    const productCount = $('#product_count').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
        if  (res.status === 'success') {
            showNotification('محصول شما با موفقیت به سبد خرید اضافه شد');
        }
    });
}

function removeOrderDetail(detailId) {
    $.get('/order/cart/remove-order-detail?detail_id=' + detailId).then(res => {
        if(res.status === 'success') {
            $('#cart-detail').html(res.data);
        }
    })
}

function changeOrderDetailCount(detailId, state) {
    const input = document.getElementById(`product_count_${detailId}`);

    let count = parseInt(input.value);

    if (state === "increase" && count < parseInt(input.max)) {
        input.value = count + 1
    }

    if (state === "decrease" && count > parseInt(input.min)) {
        input.value = count - 1;
    }
    console.log(detailId, state, input.value)
    $.get('/order/cart/change-order-count?detail_id=' + detailId + '&state=' + state).then(res => {
        if(res.status === 'success') {
            $('#cart-detail').html(res.data);
        }
    })
}


function articleCat(catId) {
    console.log(catId);
    $.get('/blog/cat?cat_id=' + catId).then(res => {
        if(res.status === 'ok') {
            $('#article_list').html(res.data);
        }
    })
}