const numbers = [1,2,3]

numbers.forEach( (n) => {
    console.log(n)
})

const x = numbers.map( (n) => {
    return n+1
})

console.log(x)