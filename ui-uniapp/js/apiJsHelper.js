//AI分析-作文数据到post数据


//AI分析-返回数据到AIcomment
export const zuowenPostResultToAiComment = (postResult)=>{
	console.log(postResult)
	let aiComment = ``
	aiComment += '总分：' + Number(postResult.compositionDetail.contentScore + postResult.compositionDetail.structureScore + postResult.compositionDetail.syntaxScore) + ' / ' + postResult.score + '\n\n'
	aiComment += '内容得分：' + postResult.compositionDetail.contentScore + '\n'
	aiComment += '内容分析：' + postResult.compositionDetail.contentComment + '\n\n'
	aiComment += '结构得分：' + postResult.compositionDetail.structureScore + '\n'
	aiComment += '结构分析：' + postResult.compositionDetail.structureComment + '\n\n'
	aiComment += '语法得分：' + postResult.compositionDetail.syntaxScore + '\n'
	aiComment += '语法分析：' + postResult.compositionDetail.syntaxComment + '\n'
	return aiComment
}

export const fanyiPostResultToAiComment = (postResult)=>{
	console.log(postResult)
}

//错题tabbar-处理数据
export const tagsPostToTags = (tagsPost)=>{
	let returnData = {
		yicuo:[],
		tixing: [],
		lingyu: [],
	}
	for (let s of tagsPost.category) {
		
		returnData.tixing.push({
			value: s,
			label: s === 'zuowen' ? '作文' :
				   s === 'yuedu' ? '阅读' :
				   s === 'fanyi' ? '翻译' :
				   s === 'xuanze' ? '选择' :
				   '未知类型'
		})
	}
	for (let s of tagsPost.falseReason) {
		returnData.yicuo.push({
			value: s.id,
			label: s.falseReason
		})
	}
	for (let s of tagsPost.field) {
		returnData.lingyu.push({
			value: s,
			label: s
		})
	}
	return returnData
	
}