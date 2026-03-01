const cocktailData = {
    recipes: [
        {
            name: "莫吉托",
            baseSpirit: "rum",
            taste: "sweet",
            mixer: "soda",
            method: "build",
            ingredients: [
                "45ml 白朗姆酒",
                "30ml 青柠汁",
                "15ml 糖浆",
                "6-8片薄荷叶",
                "苏打水补充",
                "冰块"
            ],
            description: "清新提神的经典鸡尾酒，口感清爽，带有薄荷的香气和柑橘的酸甜。",
            image: "https://images.unsplash.com/photo-1551538827-9c037cb4f32a"
        },
        {
            name: "马丁尼",
            baseSpirit: "gin",
            taste: "bitter",
            mixer: "none",
            method: "stir",
            ingredients: [
                "60ml 金酒",
                "10ml 干苦艾酒",
                "橄榄装饰",
                "柠檬皮精油"
            ],
            description: "干净利落的经典鸡尾酒，充满了金酒的草本香气和干苦艾酒的复杂味道。",
            image: "https://images.unsplash.com/photo-1575023782549-62ca0d244b39"
        },
        {
            name: "血腥玛丽",
            baseSpirit: "vodka",
            taste: "spicy",
            mixer: "juice",
            method: "build",
            ingredients: [
                "45ml 伏特加",
                "90ml 番茄汁",
                "15ml 柠檬汁",
                "辣酱",
                "黑胡椒",
                "盐"
            ],
            description: "营养丰富的开胃鸡尾酒，辛辣刺激，富含番茄的鲜美。",
            image: "https://images.unsplash.com/photo-1541546339599-ecdbfcf77378"
        },
        {
            name: "长岛冰茶",
            baseSpirit: "vodka",
            taste: "sweet",
            mixer: "soda",
            method: "build",
            ingredients: [
                "15ml 伏特加",
                "15ml 金酒",
                "15ml 朗姆酒",
                "15ml 龙舌兰",
                "15ml 君度橙酒",
                "30ml 柠檬汁",
                "30ml 糖浆",
                "可乐补充"
            ],
            description: "多种基酒的完美融合，口感醇厚，带有柑橘和可乐的甜味。",
            image: "https://images.unsplash.com/photo-1560512823-829485b8bf24"
        },
        {
            name: "玛格丽特",
            baseSpirit: "tequila",
            taste: "sour",
            mixer: "juice",
            method: "shake",
            ingredients: [
                "50ml 龙舌兰",
                "25ml 君度橙酒",
                "25ml 青柠汁",
                "盐边",
                "青柠片装饰"
            ],
            description: "墨西哥经典鸡尾酒，清爽的柑橘味道配合龙舌兰的独特风味。",
            image: "https://images.unsplash.com/photo-1556855810-ac404aa91e85"
        },
        {
            name: "威士忌酸",
            baseSpirit: "whiskey",
            taste: "sour",
            mixer: "juice",
            method: "shake",
            ingredients: [
                "60ml 波本威士忌",
                "30ml 柠檬汁",
                "15ml 糖浆",
                "1个蛋白",
                "装饰用樱桃"
            ],
            description: "经典的美式鸡尾酒，蛋白带来丝滑口感，平衡了威士忌的烈性。",
            image: "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b"
        },
        {
            name: "金汤力",
            baseSpirit: "gin",
            taste: "bitter",
            mixer: "tonic",
            method: "build",
            ingredients: [
                "45ml 金酒",
                "汤力水",
                "柠檬片",
                "迷迭香装饰"
            ],
            description: "简单而优雅的鸡尾酒，清爽的口感中带有金酒的植物香气。",
            image: "https://images.unsplash.com/photo-1558950334-8d04704332f8"
        },
        {
            name: "莓果莫斯科骡子",
            baseSpirit: "vodka",
            taste: "fruity",
            mixer: "soda",
            method: "build",
            ingredients: [
                "45ml 伏特加",
                "15ml 覆盆子糖浆",
                "30ml 青柠汁",
                "姜汁汽水",
                "新鲜覆盆子装饰"
            ],
            description: "清新的水果风味配合姜汁的辛香，既解暑又提神。",
            image: "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd"
        },
        {
            name: "尼格罗尼",
            baseSpirit: "gin",
            taste: "bitter",
            mixer: "none",
            method: "stir",
            ingredients: [
                "30ml 金酒",
                "30ml 金巴利",
                "30ml 甜苦艾酒",
                "橙皮装饰"
            ],
            description: "意大利经典开胃酒，口感复杂，带有独特的苦味和香料风味。",
            image: "https://images.unsplash.com/photo-1592858167090-2473780d894d"
        },
        {
            name: "迈泰",
            baseSpirit: "rum",
            taste: "fruity",
            mixer: "juice",
            method: "shake",
            ingredients: [
                "45ml 白朗姆酒",
                "15ml 黑朗姆酒",
                "15ml 橙酒",
                "30ml 菠萝汁",
                "30ml 橙汁",
                "15ml 青柠汁",
                "15ml 杏仁糖浆"
            ],
            description: "热带风情的水果鸡尾酒，层次丰富，充满异国情调。",
            image: "https://images.unsplash.com/photo-1549746423-e5fe9cafded8"
        },
        {
            name: "日落莫希托",
            baseSpirit: "rum",
            taste: "sweet",
            mixer: "juice",
            method: "build",
            ingredients: [
                "45ml 白朗姆酒",
                "30ml 芒果汁",
                "15ml 青柠汁",
                "15ml 糖浆",
                "6-8片薄荷叶",
                "苏打水补充",
                "新鲜芒果片装饰"
            ],
            description: "经典莫希托的热带变体，加入芒果的甜美风味。",
            image: "https://images.unsplash.com/photo-1609951651556-5334e2706168"
        },
        {
            name: "柑橘龙舌兰日落",
            baseSpirit: "tequila",
            taste: "fruity",
            mixer: "juice",
            method: "shake",
            ingredients: [
                "45ml 龙舌兰",
                "30ml 橙汁",
                "15ml 红石榴糖浆",
                "15ml 青柠汁",
                "橙片装饰"
            ],
            description: "清新的柑橘风味配合龙舌兰的草本味道，视觉效果绚丽。",
            image: "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b"
        },
        {
            name: "薄荷朱利普",
            baseSpirit: "whiskey",
            taste: "sweet",
            mixer: "none",
            method: "build",
            ingredients: [
                "60ml 波本威士忌",
                "4-5枝新鲜薄荷",
                "15ml 糖浆",
                "碎冰",
                "薄荷枝装饰"
            ],
            description: "美国南部经典鸡尾酒，清新的薄荷香气配合醇厚的威士忌。",
            image: "https://images.unsplash.com/photo-1527761939622-9119094630cf"
        }
    ],

    findCocktail(preferences) {
        return this.recipes.find(cocktail => 
            cocktail.baseSpirit === preferences.baseSpirit &&
            cocktail.taste === preferences.taste &&
            cocktail.mixer === preferences.mixer &&
            cocktail.method === preferences.method
        ) || this.getRandomCocktail(preferences);
    },

    getRandomCocktail(preferences) {
        // 如果没有完全匹配的配方，返回一个基于基酒相同的随机配方
        const matchingBase = this.recipes.filter(cocktail => 
            cocktail.baseSpirit === preferences.baseSpirit
        );
        
        if (matchingBase.length > 0) {
            return matchingBase[Math.floor(Math.random() * matchingBase.length)];
        }
        
        // 如果连基酒都没匹配的，随机返回一个配方
        return this.recipes[Math.floor(Math.random() * this.recipes.length)];
    }
}; 