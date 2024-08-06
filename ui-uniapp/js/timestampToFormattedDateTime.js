// timestampToFormattedDateTime.js

/**
 * 将时间戳转换为指定格式的日期时间字符串
 * @param {number} timestamp 要转换的时间戳
 * @returns {string} 格式化后的日期时间字符串，格式为"YYYY-MM-DD HH:mm:ss"
 */
function timestampToFormattedDateTime(timestamp) {
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2);
    const day = ('0' + date.getDate()).slice(-2);
    const hours = ('0' + date.getHours()).slice(-2);
    const minutes = ('0' + date.getMinutes()).slice(-2);
    const seconds = ('0' + date.getSeconds()).slice(-2);

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

export default timestampToFormattedDateTime;
