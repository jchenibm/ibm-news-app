<template>
  <div class="news-card">
    <a :href="news.url" target="_blank">
      <img :src="news.image || defaultImage" alt="News Image" class="news-image">
    </a>
    <div class="news-content">
      <a :href="news.url" target="_blank" class="news-title">
        <h3>{{ news.title }}</h3>
      </a>
      <div :class="['news-summary', { scrollable: isScrollable }]">
        <p>{{ news.summary }}</p>
      </div>
      <a :href="news.url" target="_blank" class="read-more">Read more</a>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    news: Object
  },
  data() {
    return {
      isScrollable: false // State to track if the summary is scrollable
    };
  },
  computed: {
    defaultImage() {
      return '/IBM Logo.png'; // Path to the default image in the public directory
    }
  },
  methods: {
    toggleScroll() {
      this.isScrollable = !this.isScrollable; // Toggle the scrollable state
    }
  }
}
</script>

<style scoped>
.news-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  margin: 10px;
  display: flex;
  flex-direction: column;
  max-width: 300px;
  height: 400px; /* Set a fixed height for consistency */
  cursor: pointer; /* Indicate that the card is clickable */
}

.news-image {
  width: 100%;
  height: 150px; /* Set a fixed height for the image */
  object-fit: cover; /* Ensure the image covers the area */
}

.news-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex-grow: 1;
  padding: 10px;
  overflow: hidden; /* Hide overflow by default */
}

.news-title {
  text-decoration: none;
  color: inherit; /* Inherit color from parent */
}

.news-title:hover {
  text-decoration: underline;
}

.news-summary {
  flex-grow: 1;
  overflow-y: hidden; /* Hide scrollbar by default */
  margin-bottom: 10px; /* Add some space between summary and read more link */
  transition: overflow 0.3s; /* Smooth transition for scrollbar appearance */
}

.news-summary.scrollable {
  overflow-y: auto; /* Enable vertical scrolling when scrollable */
}

.read-more {
  text-align: center; /* Center the text */
  text-decoration: none;
  color: #007bff;
  font-weight: bold;
}

.read-more:hover {
  text-decoration: underline;
}
</style>
