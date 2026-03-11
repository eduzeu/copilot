


const login = () => {
  return (
    <div>
      <h1> Login </h1>
      <form>
        <label htmlFor="email">Email:</label>
        <input type="text" id="username" name="username" />
        <label htmlFor="password">Password:</label>
        <input type="password" id="password" name="password" />
        <button type="submit">Login</button>
      </form>
    </div>
  )
}


export default login;