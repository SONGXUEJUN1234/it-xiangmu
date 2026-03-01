document.addEventListener('DOMContentLoaded', () => {
    const cocktailForm = document.getElementById('cocktailForm');
    const resultSection = document.getElementById('result');
    const cocktailImage = document.querySelector('.cocktail-image');
    const cocktailName = document.getElementById('cocktailName');
    const recipeList = document.getElementById('recipeList');
    const tasteDescription = document.getElementById('tasteDescription');
    const stars = document.querySelectorAll('.star');
    const submitRatingBtn = document.getElementById('submitRating');
    let currentRating = 0;

    // 处理表单提交
    cocktailForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const formData = new FormData(cocktailForm);
        const preferences = {
            baseSpirit: formData.get('baseSpirit'),
            taste: formData.get('taste'),
            mixer: formData.get('mixer'),
            method: formData.get('method')
        };

        const cocktail = cocktailData.findCocktail(preferences);
        displayCocktail(cocktail);
    });

    // 显示鸡尾酒信息
    function displayCocktail(cocktail) {
        // 显示结果区域
        resultSection.style.display = 'block';

        // 设置鸡尾酒图片
        cocktailImage.innerHTML = `<img src="${cocktail.image}" alt="${cocktail.name}">`;

        // 设置鸡尾酒名称
        cocktailName.textContent = cocktail.name;

        // 设置配方列表
        recipeList.innerHTML = cocktail.ingredients
            .map(ingredient => `<li>${ingredient}</li>`)
            .join('');

        // 设置口味描述
        tasteDescription.textContent = cocktail.description;

        // 重置评分
        resetRating();
    }

    // 处理星级评分
    stars.forEach(star => {
        star.addEventListener('click', (e) => {
            const rating = parseInt(e.target.dataset.rating);
            currentRating = rating;
            updateRating(rating);
        });

        star.addEventListener('mouseover', (e) => {
            const rating = parseInt(e.target.dataset.rating);
            highlightStars(rating);
        });

        star.addEventListener('mouseout', () => {
            highlightStars(currentRating);
        });
    });

    // 更新评分显示
    function updateRating(rating) {
        stars.forEach(star => {
            const starRating = parseInt(star.dataset.rating);
            if (starRating <= rating) {
                star.classList.add('active');
                star.style.color = '#f1c40f';
            } else {
                star.classList.remove('active');
                star.style.color = '#ddd';
            }
        });
    }

    // 高亮显示星星
    function highlightStars(rating) {
        stars.forEach(star => {
            const starRating = parseInt(star.dataset.rating);
            star.style.color = starRating <= rating ? '#f1c40f' : '#ddd';
        });
    }

    // 重置评分
    function resetRating() {
        currentRating = 0;
        stars.forEach(star => {
            star.classList.remove('active');
            star.style.color = '#ddd';
        });
    }

    // 处理评分提交
    submitRatingBtn.addEventListener('click', () => {
        if (currentRating === 0) {
            alert('请先选择评分！');
            return;
        }

        alert(`感谢您的评分：${currentRating}星！`);
        resetRating();
    });
}); 