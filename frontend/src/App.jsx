import { useMemo, useState } from 'react';

const initialPost = {
  topic: '',
  tone: 'professional',
  caption: '',
  hashtags: [],
  imageUrl: '',
  createdAt: ''
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000';

function normalizePostPayload(payload, topic, tone) {
  const hashtags = Array.isArray(payload?.hashtags)
    ? payload.hashtags
    : typeof payload?.hashtags === 'string'
      ? payload.hashtags.split(/[\s,]+/).filter(Boolean)
      : [];

  return {
    topic,
    tone,
    caption: payload?.caption ?? '',
    hashtags: hashtags.slice(0, 10),
    imageUrl: payload?.imageUrl || payload?.image || payload?.image_url || '',
    createdAt: new Date().toISOString()
  };
}

export default function App() {
  const [topic, setTopic] = useState('');
  const [tone, setTone] = useState('professional');
  const [post, setPost] = useState(initialPost);
  const [savedPosts, setSavedPosts] = useState([]);
  const [loadingGenerate, setLoadingGenerate] = useState(false);
  const [loadingPost, setLoadingPost] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const captionWordCount = useMemo(() => {
    return post.caption.trim() ? post.caption.trim().split(/\s+/).length : 0;
  }, [post.caption]);

  const canGenerate = topic.trim().length > 0 && !loadingGenerate;
  const canSimulate = post.caption && !loadingPost;

  const clearMessages = () => {
    setError('');
    setSuccess('');
  };

  const generatePost = async (event) => {
    event.preventDefault();
    clearMessages();
    setLoadingGenerate(true);

    try {
      const response = await fetch(`${API_BASE_URL}/generate-post`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ topic, tone })
      });

      if (!response.ok) {
        throw new Error(`Generate failed with status ${response.status}`);
      }

      const data = await response.json();
      const normalized = normalizePostPayload(data, topic, tone);

      if (!normalized.caption) {
        throw new Error('No caption was returned by the API.');
      }

      setPost(normalized);
      setSuccess('Post generated successfully. You can now simulate publishing.');
    } catch (requestError) {
      setError(requestError.message || 'Unable to generate post right now.');
    } finally {
      setLoadingGenerate(false);
    }
  };

  const simulatePost = async () => {
    clearMessages();
    setLoadingPost(true);

    try {
      const response = await fetch(`${API_BASE_URL}/post`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(post)
      });

      if (!response.ok) {
        throw new Error(`Post simulation failed with status ${response.status}`);
      }

      const saved = await response.json();
      setSavedPosts((current) => [saved, ...current]);
      setSuccess('Post simulated and stored successfully.');
    } catch (requestError) {
      setError(requestError.message || 'Unable to simulate posting.');
    } finally {
      setLoadingPost(false);
    }
  };

  return (
    <div className="page">
      <header>
        <h1>AI Instagram Post Generator</h1>
        <p>
          Generate AI captions + images and simulate Instagram posting using
          your backend endpoints.
        </p>
      </header>

      <main className="layout">
        <section className="panel">
          <h2>Create a Post</h2>
          <form onSubmit={generatePost} className="form">
            <label htmlFor="topic">Topic</label>
            <input
              id="topic"
              type="text"
              value={topic}
              onChange={(event) => setTopic(event.target.value)}
              placeholder="e.g. Work from home productivity"
              required
            />

            <label htmlFor="tone">Tone</label>
            <select
              id="tone"
              value={tone}
              onChange={(event) => setTone(event.target.value)}
            >
              <option value="professional">Professional</option>
              <option value="casual">Casual</option>
            </select>

            <button type="submit" disabled={!canGenerate}>
              {loadingGenerate ? 'Generating...' : 'Generate Post'}
            </button>
          </form>

          {error ? <p className="status error">{error}</p> : null}
          {success ? <p className="status success">{success}</p> : null}
        </section>

        <section className="panel preview-panel">
          <h2>Instagram Preview (Simulation)</h2>
          <article className="insta-card" aria-live="polite">
            <div className="insta-header">
              <div className="avatar" aria-hidden="true" />
              <div>
                <strong>ai_post_bot</strong>
                <p>{post.topic || 'No topic yet'}</p>
              </div>
            </div>

            <div className="insta-image-wrap">
              {post.imageUrl ? (
                <img src={post.imageUrl} alt={`Generated visual for ${post.topic}`} />
              ) : (
                <div className="image-placeholder">Generated image will appear here.</div>
              )}
            </div>

            <div className="insta-body">
              <p className="caption">
                {post.caption || 'Generate a post to preview the caption here.'}
              </p>
              <p className="meta">Caption words: {captionWordCount} / 150 max</p>
              <p className="hashtags">
                {post.hashtags.length > 0
                  ? post.hashtags.map((tag) =>
                      tag.startsWith('#') ? tag : `#${tag}`
                    ).join(' ')
                  : '#hashtags #will #appear #here'}
              </p>
            </div>
          </article>

          <button className="secondary" onClick={simulatePost} disabled={!canSimulate}>
            {loadingPost ? 'Posting...' : 'Simulate Post (/post)'}
          </button>
        </section>

        <section className="panel">
          <h2>Stored Simulated Posts</h2>
          {savedPosts.length === 0 ? (
            <p className="empty">No posts stored yet.</p>
          ) : (
            <ul className="saved-list">
              {savedPosts.map((saved, index) => (
                <li key={saved.id || `${saved.createdAt || 'saved'}-${index}`}>
                  <strong>{saved.topic || post.topic || 'Untitled Topic'}</strong>
                  <span>{saved.tone || post.tone}</span>
                  <p>{saved.caption || post.caption}</p>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  );
}
