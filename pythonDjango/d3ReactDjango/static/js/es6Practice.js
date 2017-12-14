var pizza = true
pizza = false 
console.log(pizza) // false

const pizza2 = false


// lexical variable scoping
var topic = "JavaScript"
if (topic) {
	var topic = "React" console.log('block', topic)	// block React
}

console.log('global', topic) // global React

