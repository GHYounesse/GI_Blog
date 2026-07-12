import { useEffect, useState } from "react";
import API from "../api/axios";
import { Post } from "../types/index";

export default function Home() {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    API.get("posts/")
      .then((res) => setPosts(res.data.results))
      .catch((err) => console.log(err));
  }, []);

  return (
    <div>
      <h1>Posts</h1>

      {posts.map((post) => (
        <div key={post.id}>
          <h3>{post.title}</h3>
          <p>{post.content}</p>
          <p>❤️ {post.total_likes}</p>
        </div>
      ))}
    </div>
  );
}
