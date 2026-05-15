export const PHOTOS_QUERY = `
  query {
    photos {
      id
      image
      caption
      tags
      likesCount
      comments {
        id
        text
        author {
          username
        }
      }
    }
  }
`;

export const SEARCH_PHOTOS_QUERY = `
  query($query: String!) {
    searchPhotos(query: $query) {
      id
      image
      caption
      tags
      likesCount
      comments {
        id
        text
        author {
          username
        }
      }
    }
  }
`;