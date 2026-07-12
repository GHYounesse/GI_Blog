export interface User {
  id: number;
  username: string;
}

export interface Post {
  id: number;
  title: string;
  content: string;
  image?: string;
  author: User;
  total_likes: number;
  is_liked: boolean;
}
