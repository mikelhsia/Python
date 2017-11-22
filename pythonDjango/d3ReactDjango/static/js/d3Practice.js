/*
datum()：绑定一个数据到选择集上
data()：绑定一个数组到选择集上，数组的各项值分别与选择集的各元素绑定
*/

/* JavaScript Ajax 动态刷新页面
 * 网页前台使用Ajax发送请求，后台处理数据后返回数据给前台，前台不刷新网页动态加载数据
 * JS 发送ajax请求，后台处理请求并返回status, result
 * 在 success: 后面定义回调函数处理返回的数据，需要使用 JSON.parse(data)
 * This is jQuery ajax method
 */
function getStockHisData(code) {
	var post_data = {
		"code": code
	};

	var price;

	d = $.ajax({
		url: 'dataset',
		type: "POST",
		data: post_data,
		// 阻塞同步
		async: false,
		success: function (data) {
			data = JSON.parse(data);
			if (data) {
				price = data;
			} else {
				dataset = "";
				alert("No Data");
			}
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			alert("Ajax failed: "+ XMLHttpRequest.readyState + " (" + XMLHttpRequest.status + ") " + textStatus);
		}
	});

	return price;
}
dataset = getStockHisData('601899');

var str = "China";

var body = d3.select("body");
var p = body.selectAll("p");

p.datum(str);

p.text(function(d, i){
	/*
	用到了一个无名函数 function(d, i)。当选择集需要使用被绑定的数据时，常需要这么使用。其包含两个参数，其中：
		d 代表数据，也就是与某元素绑定的数据。
		i 代表索引，代表数据的索引号，从 0 开始。
	*/
    return "第 "+ i + " 个元素绑定的数据是 " + d;
});


var dSet = [ "I like dog",
				"I like cat",
				"I like snake"];

p.data(dSet)
  .text(function(d, i) {
		return d;
  });


var t = d3.select("body").select("p")
t.style("color","red")


var width = 300;  //画布的宽度
var height = 300;   //画布的高度

var svg = d3.select(".my-canvas")     //选择文档中的body元素
    .append("svg")          //添加一个svg元素
    .attr("width", width)       //设定宽度
    .attr("height", height);    //设定高度

//var dataset = [ 250 , 210 , 170 , 130 , 90 ];  //数据（表示矩形的宽度）
// Now I'm getting data from home.html {{byd_close_list}}
var rectHeight = 4;   //每个矩形所占的像素高度(包括空白)

/*********************************************************
 * 有数据，而没有足够图形元素的时候，使用此方法可以添加足够的元素。
 * 如果数组为 [3, 6, 9, 12, 15]，将此数组绑定到三个 p 元素的选择集上。
 * 可以想象，会有两个数据没有元素与之对应，这时候 D3 会建立两个空的元素与数据对应，这一部分就称为 Enter。
 * 而有元素与数据对应的部分称为 Update。
 * 如果数组为 [3]，则会有两个元素没有数据绑定，那么没有数据绑定的部分被称为 Exit。
 * update 部分的处理办法一般是：更新属性值
 * enter 部分的处理办法一般是：添加元素后，赋予属性值
 *********************************************************
 * var dataset = [ 3 , 6 , 9 , 12 , 15 ];
 * 
 * //选择body中的p元素
 * var p = d3.select("body").selectAll("p");
 * 
 * //获取update部分
 * var update = p.data(dataset);
 * 
 * //获取enter部分
 * var enter = update.enter();
 * 
 * //update部分的处理：更新属性值
 * update.text(function(d){
 *     return "update " + d;
 * });
 * 
 * //enter部分的处理：添加元素后赋予属性值
 * enter.append("p")
 *     .text(function(d){
 *         return "enter " + d;
 *     });
 * 
 *  //获取exit部分
 * var exit = update.exit();
 * 
 * //update部分的处理：更新属性值
 * update.text(function(d){
 *     return "update " + d;
 * });
 * 
 * //exit部分的处理：修改p元素的属性
 * exit.text(function(d){
 *         return "exit";
 *     });
 * 
 * //exit部分的处理通常是删除元素
 * // exit.remove();
 *********************************************************/
svg.selectAll("rect")		// 选择svg内所有的矩形
    .data(dataset)			// 绑定数组
    .enter()				// 指定选择集的enter部分
    .append("rect")			// 添加足够数量的矩形元素
    .attr("x",20)
    .attr("y",function(d,i){
         return i * rectHeight;
    })
    .attr("width",function(d){
         return d;
    })
    .attr("height",rectHeight-2)
    .attr("fill","steelblue");


/*********************************************************
 * 比例尺（Scale）：
 * 将某一区域的值映射到另一区域，其大小关系不变。
 *********************************************************/
// 线性比例尺，能将一个连续的区间，映射到另一区间。要解决柱形图宽度的问题，就需要线性比例尺。
// 要求：将 dataset 中最小的值，映射成 0；将最大的值，映射成 300。
var dataset = [1.2, 2.3, 0.9, 1.5, 3.3];

var min = d3.min(dataset);		// 这两个函数能够求数组的最大值和最小值
var max = d3.max(dataset);

var linear = d3.scaleLinear()	// d3.scalelinear() 返回一个线性比例尺。domain() 和 range() 分别设定比例尺的定义域和值域。
        .domain([min, max])		// 比例尺的定义域 domain 为：[0.9, 3.3]
        .range([0, 300]);		// 比例尺的值域 range 为：[0, 300]

// d3.scale.linear() 的返回值，是可以当做函数来使用的
linear(0.9);    //返回 0
linear(2.3);    //返回 175
linear(3.3);    //返回 300

// 序数比例尺，有时候，定义域和值域不一定是连续的
// 要求：我们希望 0 对应颜色 red，1 对应 blue，依次类推
var index = [0, 1, 2, 3, 4];
var color = ["red", "blue", "green", "yellow", "black"];

var ordinal = d3.scaleOrdinal()
        .domain(index)
        .range(color);

ordinal(0); //返回 red
ordinal(2); //返回 green
ordinal(4); //返回 black


// 给柱形图添加比例尺
var dataset = [ 2.5 , 2.1 , 1.7 , 1.3 , 0.9 ];

var linear = d3.scaleLinear()
        .domain([0, d3.max(dataset)])
        .range([0, 250]);


// 按照上一章的方法添加矩形，在给矩形设置宽度的时候，应用比例尺。
var rectHeight = 25;   //每个矩形所占的像素高度(包括空白)

var rects = svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect")
    .attr("x",20)
    .attr("y",function(d,i){
         return i * rectHeight;
    })
    .attr("width",function(d){
         return linear(d);   //在这里用比例尺
    })
    .attr("height",rectHeight-2)
    .attr("fill","steelblue");


/*
 * 我们需要用其他元素来组合成坐标轴，最终使其变为类似以下的形式：
 * <g>
 * <!-- 第一个刻度 -->
 * <g>
 * <line></line>   <!-- 第一个刻度的直线 -->
 * <text></text>   <!-- 第一个刻度的文字 -->
 * </g>
 * <!-- 第二个刻度 -->
 * <g>
 * <line></line>   <!-- 第二个刻度的直线 -->
 * <text></text>   <!-- 第二个刻度的文字 -->
 * </g> 
 * ...
 * <!-- 坐标轴的轴线 -->
 * <path></path>
 * </g>
 * 分组元素 ，是 SVG 画布中的元素，意思是 group。此元素是将其他元素进行组合的容器，在这里是用于将坐标轴的其他元素分组存放。
 * 如果需要手动添加这些元素就太麻烦了，为此，D3 提供了一个组件：d3.svg.axis()。它为我们完成了以上工作。
 */

//数据
var dataset = [2.5 , 2.1 , 1.7 , 1.3 , 0.9];
//定义比例尺
var linear = d3.scaleLinear()
     .domain([0, d3.max(dataset)])
     .range([0, 250]);

var axis = d3.axisBottom()	// D3 中坐标轴的组件，能够在 SVG 中生成组成坐标轴的元素。指定刻度的方向
     .scale(linear)			//指定比例尺
     .ticks(7);				//指定刻度的数量

svg.append("g")
     .attr("class","axis")
     .attr("transform","translate(20,130)")
     .call(axis);		// call() 的参数是一个函数。调用之后，将当前的选择集作为参数传递给此函数。

/* 也就是说，以下两个代码是相等的
 * function foo(selection) {
 *   selection
 *     .attr("name1", "value1")
 *     .attr("name2", "value2");
 * }
 * foo(d3.selectAll("div"))
 * *******************************
 * d3.selectAll("div").call(foo);
 * *******************************
 */


/*********************************************************
 * 完整的柱形图：
 * 1. 添加 SVG 画布
 * 2. 定义数据和比例尺
 *********************************************************/
// 画布大小
var width = height = 400;

// 在 body 里添加一个 SVG 画布   
var svgHist = d3.select("#svgHist")
			.append("svg")
			.attr("class","svgHist")
			.attr("width", width)
			.attr("height", height)
			.attr("padding", height/2);


// 画布周边的空白
var padding = {left:30, right:30, top:20, bottom:20};

// 定义数据
var dataset = [10, 20, 30, 40, 33, 24, 12, 5];

// 定义比例尺
var xScale = d3.scaleBand()
			.domain(d3.range(dataset.length))
			.rangeRound([0, width - padding.left - padding.right]);

var yScale = d3.scaleLinear()
			.domain([0, d3.max(dataset)])
			.range([height - padding.top - padding.bottom, 0]);

// 定义坐标轴
var xAxis = d3.axisBottom().scale(xScale);
var yAxis = d3.axisLeft().scale(yScale);

// 矩形之间的空白
var rectPadding = 4;

// 添加矩形元素
var rects = svgHist.selectAll(".my-hist-rect")
				.data(dataset)
				.enter()
				.append("rect")
				.attr("class","my-hist-rect")
				.attr("transform", "translate(" + padding.left + "," + padding.top + ")")
				.attr("x", function(d, i) {
					return xScale(i) + rectPadding/2;
				})
				.attr("width", xScale.bandwidth() - rectPadding)
				.attr("fill","steelblue")
				// .attr("height", function(d) {
				// 	return 0;
				// })
				// .attr("y", function(d, i) {
				// 	var min = yScale.domain()[0];
				//     return yScale(min);
				// })
				// .transition()
				// .delay(function(d, i) {
    // 				return i * 200;
				// })
				// .duration(2000)
				// .ease(d3.easeBounce)
				/***************************************************
				 * Transition and the event can't work at the same time.
  				 ***************************************************/
				.attr("y", function(d, i) {
					return yScale(d);
				})
				.attr("height", function(d) {
					return height - padding.top - padding.bottom - yScale(d);
				})
				.on("mouseover", function(d, i) {
					d3.select(this)
						.attr("fill","purple");
				})
				.on("mouseout", function(d, i) {
					d3.select(this)
						.transition()
						.duration(500)
						.attr("fill","steelblue");
				});

// 添加文字元素
var texts = svgHist.selectAll(".my-hist-text")
				.data(dataset)
				.enter()
				.append("text")
				.attr("class", "my-hist-text")
				.attr("transform", "translate(" + padding.left + ", " + padding.top + ")")
				.attr("x", function(d, i) {
					return xScale(i) + rectPadding/3;
				})
				.attr("y", function(d, i) {
					// return yScale(d);
					var min = yScale.domain()[0];
				    return yScale(min);
				})
				.attr("dx", function(d, i) {
					return (xScale.bandwidth() - rectPadding)/2;
				})
				.attr("dy", function(d, i) {
					return 20;
				})
				.text(function(d) {
					return d;
				})
				.attr("fill", "white")
				.transition()
				.delay(function(d, i) {
    				return i * 200;
				})
				.duration(2000)
				.ease(d3.easeBounce)
				.attr("y", function(d, i) {
					return yScale(d);
				});

// 添加x轴
svgHist.append("g")
	.attr("class", "axis")
	.attr('transform', 'translate(' + padding.left + ',' + (height - padding.bottom) + ')')
	.call(xAxis);

// 添加y轴
svgHist.append("g")
	.attr("class", "axis")
	.attr('transform', 'translate(' + padding.left + ',' + padding.top + ')')
	.call(yAxis);


/*********************************************************
 * 过渡动画（Animation）:
 * transition()
 * duration():
 * ease()
 * * circleTransition(d3.easeElastic,0);
 * * circleTransition(d3.easeBounce,1);
 * * circleTransition(d3.easeLinear,2);
 * * circleTransition(d3.easeSin,3);
 * * circleTransition(d3.easeQuad,4);
 * * circleTransition(d3.easeCubic,5);
 * * circleTransition(d3.easePoly,6);
 * * circleTransition(d3.easeCircle,7);
 * * circleTransition(d3.easeExp,8);
 * * circleTransition(d3.easeBack,9);
 * delay()
 *********************************************************/
// 下面将在 SVG 画布里添加三个圆，圆出现之后，立即启动过渡效果。

var svgCircleTransition = d3.select("#circle-animation")
							.append("svg")
							.attr("width", width)
							.attr("height", height);

var circle1 = svgCircleTransition.append("circle")
								.attr("cx", 100)
								.attr("cy", 100)
								.attr("r", 45)
								.style("fill", "green");

//在1秒（1000毫秒）内将圆心坐标由100变为300
circle1.transition()
	.duration(2000)
	.ease(d3.easeBounce)
	.attr("cx", 300)
	.style("fill", "red");

/*
 * on() 的第一个参数是监听的事件，第二个参数是监听到事件后响应的内容，第二个参数是一个函数。
 * 鼠标常用的事件有：
 * click：鼠标单击某元素时，相当于 mousedown 和 mouseup 组合在一起。
 * mouseover：光标放在某元素上。
 * mouseout：光标从某元素上移出来时。
 * mousemove：鼠标被移动的时候。
 * mousedown：鼠标按钮被按下。
 * mouseup：鼠标按钮被松开。
 * dblclick：鼠标双击。
 * 
 * 键盘常用的事件有三个：
 * keydown：当用户按下任意键时触发，按住不放会重复触发此事件。该事件不会区分字母的大小写，例如“A”和“a”被视为一致。
 * keypress：当用户按下字符键（大小写字母、数字、加号、等号、回车等）时触发，按住不放会重复触发此事件。该事件区分字母的大小写。
 * keyup：当用户释放键时触发，不区分字母的大小写。 触屏常用的事件有三个：
 * * touchstart：当触摸点被放在触摸屏上时。
 * * touchmove：当触摸点在触摸屏上移动时。
 * * touchend：当触摸点从触摸屏上拿开时。 
 * 
 * 当某个事件被监听到时，D3 会把当前的事件存到 d3.event 对象，
 * 里面保存了当前事件的各种参数，请大家好好参详。
 * 如果需要监听到事件后立刻输出该事件，可以添加一行代码： console.log(d3.event);
 */
circle1.on(d3.mouseover, function(d, i) {
	console.log(d3.event);
});


var circle2 = svgCircleTransition.append("circle")
								.attr("cx", 100)
								.attr("cy", 100)
								.attr("r", 45)
								.style("fill", "green");

//在1秒（1000毫秒）内将圆心坐标由100变为300
circle2.transition()
	.duration(1500)
	.attr("cy", 300);

var circle3 = svgCircleTransition.append("circle")
								.attr("cx", 100)
								.attr("cy", 100)
								.attr("r", 45)
								.style("fill", "green");

//在1秒（1000毫秒）内将圆心坐标由100变为300
circle3.transition()
	.duration(2300)
	.ease(d3.easeElasticIn)
	.attr("cx", 300)
	.attr("cy", 300)
	.style("fill", "red")
	.attr("r",20);
