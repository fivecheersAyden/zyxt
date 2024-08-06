// questypeTranslator.js

/**
 * 将拼音的题型转化为汉字
 * @param {string} input 要转换的题型拼音
 * @param {string} mode 要转换的模式，"zh"表示转换为汉字，"en"表示转换为拼音
 * @returns {string} 转换后的题型汉字
 */

function quesTypeTranslator(input, mode = "zh") {
    if(mode === "zh") {
        const mapping1 = {
            "xuanze": "选择",
            "yuedu": "阅读",
            "fanyi": "翻译",
            "zuowen": "作文"
        };

        // 检查输入是否在映射中，如果在则返回对应的值，否则返回原始值
        return mapping1[input] || input;
    } else if(mode === "en") {
        const mapping2 = {
            "选择": "xuanze",
            "阅读": "yuedu",
            "翻译": "fanyi",
            "作文": "zuowen"
        };
        return mapping2[input] || input;
    }
}

export default quesTypeTranslator;