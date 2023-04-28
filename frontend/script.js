
const form = document.querySelector('#form')
const usernameField = document.querySelector('#username')
const passwordField = document.querySelector('#password')
const inputField = document.querySelector('#input')
const promptField = document.querySelector('#prompt')
const trainField = document.querySelector('#train')
const testField = document.querySelector('#test')
const feedbackField = document.querySelector('#feedback')
const testCount = document.getElementById('count')
const consentFields = [...document.querySelectorAll('label > input[type=checkbox]')]

const prompt = promptField.value

const keysAllowed = new Set(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,')
const keylog = []
let input = ''
let count = 0

//Enable input field
const enableInput = () => {
	let readOnly = false
	readOnly ||= usernameField.value.length === 0
	readOnly ||= passwordField.value.length === 0
	readOnly ||= consentFields.filter(f => !f.checked).length !== 0
	inputField.readOnly = readOnly
}

//Clear input field
const resetInput = () => {
	// console.log('reset')
	keylog.length = 0
	input = ''
	inputField.value = input
	inputField.classList.remove('correct')
	enableInput()
}

//Reset counter
const resetCount = () => {
	count = 0
	testCount.innerHTML = count.toString()
}


[usernameField, passwordField, ...consentFields].forEach(field => {
	field.addEventListener('input', (event) => {
		resetInput()
		resetCount()
	})
})


inputField.addEventListener('blur', (event) => {
	resetInput()
})

//Only allow input entry if consent form and username and password are filled
inputField.addEventListener('click', (event) => {
	if (usernameField.value.length === 0 || passwordField.value.length === 0) {
		alert('Username and password cannot be empty.')
		return
	}

	// console.log(consentFields.filter(f => !f.checked).length)

	if (consentFields.filter(f => !f.checked).length !== 0) {
		alert('Fill the consent form to continue.')
		return
	}
})

//Run a series of processes on every key press
inputField.addEventListener('keydown', (event) => {
	event.preventDefault()

	const { key, timeStamp } = event

	//Check whether the character matches the prompt
	if (!keysAllowed.has(key)) return
	if (key !== prompt[input.length]) {
		inputField.classList.value = 'incorrect'
		return
	} else {
		inputField.classList.value = 'correct'
	}

	//Create a list of keytimes
	keylog.push(timeStamp)
	input += key

	inputField.value = input

	//Send submission request once sentence is entered
	if (input.length === prompt.length) {
		inputField.readOnly = true
		inputField.classList.value = 'correct'
		form.requestSubmit()
	}
})


//Send request to backend, compiling data
const sendRequest = async (data) => {
	// console.log(data)
	// console.log(data.keytimes.length, prompt.length)

	// const URL = "http://localhost:8000/sample/"
	const URL = "https://keystrokeauth.orebenson.com/sample/"
	// const URL = "https://3.8.102.0/sample/"

	const response = await fetch(URL, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({
			...data
		})
	})
	const json = await response.json()
	// const json = {status: 'good', message:'banana'}

	resetInput()

	//Receive status messages from backend and display to user
	if (json.status === 'good') {
		feedbackField.value = json.message
		feedbackField.className = 'correct'
	} else if (json.status === 'bad') {
		feedbackField.value = json.message
		feedbackField.className = 'error'
	}
}

//Executes submission function on the form
form.addEventListener('submit', (event) => {
	event.preventDefault()

	const username = usernameField.value
	const password = passwordField.value
	const train = trainField.checked
	// const train = true

	const firstKey = keylog[0]
	const keytimes = keylog.map(key => key - firstKey)

	// console.log(keytimes.length)

	sendRequest({ username, password, keytimes, train })

	count += 1
	testCount.innerHTML = count.toString()

})

