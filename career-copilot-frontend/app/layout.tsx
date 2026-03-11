import Link from 'next/link';
import Login from './auth/login';
import Button from '../components/ui/Button';

const HomePage = () => {
  return (
    <div>
      <h1>Welcome to Career Copilot</h1>
      <Login />
      <Link href="/auth/account">
        <Button>Don't have an account yet? Create one here.</Button>
      </Link>
    </div>
  );
};

export default HomePage;