

const CreateAccount = () => {
  return (
    <div>
      <h1> Create Account </h1>
      <form>
        <label htmlFor="email">Email:</label>
        <input type="email" id="email" name="email" />
        <label htmlFor="password">Password:</label>
        <input type="password" id="password" name="password" />
        <button type="submit">Create Account</button>
      </form>
    </div>

  )
}

export default CreateAccount;
