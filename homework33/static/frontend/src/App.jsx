const {useEffect, useState} = React;

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

async function gql(query, variables = {}) {
    const response = await fetch("/graphql/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({query, variables}),
    });

    return response.json();
}

function PhotoCard({photo, onLike, onComment}) {
    const [commentText, setCommentText] = useState("");

    const submitComment = () => {
        if (!commentText.trim()) return;

        onComment(photo.id, commentText);
        setCommentText("");
    };

    return (
        <div className="card shadow-sm h-100">
            <div className="card-body">
                {photo.image ? (
                    <img
                        src={photo.image}
                        className="card-img-top rounded mb-3"
                        style={{height: 220, objectFit: "cover"}}
                        alt={photo.caption || "Фото"}
                    />
                ) : (
                    <div
                        className="bg-secondary-subtle rounded mb-3 d-flex align-items-center justify-content-center"
                        style={{height: 220}}
                    >
                        <span className="text-muted">Фото #{photo.id}</span>
                    </div>
                )}

                <h5 className="card-title">{photo.caption || "Без опису"}</h5>

                <p className="card-text small text-muted">
                    {(photo.tags || []).join(", ")}
                </p>

                <button
                    className="btn btn-outline-danger btn-sm mb-3"
                    onClick={() => onLike(photo.id)}
                >
                    ❤ {photo.likesCount}
                </button>

                <hr/>

                <h6 className="fw-bold">Коментарі</h6>

                {(photo.comments || []).length === 0 ? (
                    <p className="text-muted small mb-2">Коментарів ще немає</p>
                ) : (
                    <div className="mb-3">
                        {photo.comments.map((comment) => (
                            <div className="small mb-2" key={comment.id}>
                                <strong>{comment.author.username}:</strong>{" "}
                                {comment.text}
                            </div>
                        ))}
                    </div>
                )}

                <div className="input-group input-group-sm">
                    <input
                        className="form-control"
                        value={commentText}
                        onChange={(event) => setCommentText(event.target.value)}
                        placeholder="Додати коментар..."
                    />

                    <button className="btn btn-dark" onClick={submitComment}>
                        Надіслати
                    </button>
                </div>
            </div>
        </div>
    );
}

function ToastMessage({message, onClose}) {
    if (!message) return null;

    return (
        <div className="toast-container position-fixed top-0 end-0 p-3">
            <div className="toast show">
                <div className="toast-header">
                    <strong className="me-auto">InstaPhoto</strong>
                    <button
                        type="button"
                        className="btn-close"
                        onClick={onClose}
                    ></button>
                </div>
                <div className="toast-body">{message}</div>
            </div>
        </div>
    );
}

function UploadModal({onCreate}) {
    const [caption, setCaption] = useState("");
    const [tags, setTags] = useState("");
    const [image, setImage] = useState(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];

        if (!file) {
            setImage(null);
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            alert("Фото завелике. Обери файл до 5 MB.");
            event.target.value = "";
            setImage(null);
            return;
        }

        setImage(file);
    };

    const submit = () => {
        const cleanedTags = tags
            .split(",")
            .map((tag) => tag.trim())
            .filter(Boolean);

        if (image) {
            const reader = new FileReader();

            reader.onloadend = () => {
                onCreate(caption, cleanedTags, reader.result);
            };

            reader.readAsDataURL(image);
        } else {
            onCreate(caption, cleanedTags, null);
        }

        setCaption("");
        setTags("");
        setImage(null);
    };

    return (
        <div className="modal fade" id="uploadModal" tabIndex="-1">
            <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Завантажити фото</h5>
                        <button
                            type="button"
                            className="btn-close"
                            data-bs-dismiss="modal"
                        ></button>
                    </div>

                    <div className="modal-body">
                        <label className="form-label">Опис</label>
                        <input
                            className="form-control mb-3"
                            value={caption}
                            onChange={(event) => setCaption(event.target.value)}
                            placeholder="Наприклад: захід сонця"
                        />

                        <label className="form-label">Теги</label>
                        <input
                            className="form-control mb-3"
                            value={tags}
                            onChange={(event) => setTags(event.target.value)}
                            placeholder="nature, city"
                        />

                        <label className="form-label">Фото</label>
                        <input
                            className="form-control"
                            type="file"
                            accept="image/*"
                            onChange={handleFileChange}
                        />
                    </div>

                    <div className="modal-footer">
                        <button className="btn btn-secondary" data-bs-dismiss="modal">
                            Скасувати
                        </button>

                        <button
                            className="btn btn-primary"
                            data-bs-dismiss="modal"
                            onClick={submit}
                        >
                            Опублікувати
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

function App() {
    const [photos, setPhotos] = useState([]);
    const [search, setSearch] = useState("");
    const [toast, setToast] = useState("");

    const loadPhotos = async () => {
        const result = await gql(`
            query {
                photos {
                    id
                    image
                    caption
                    tags
                    likesCount
                }
            }
        `);

        setPhotos(result.data?.photos || []);
    };

    const createComment = async (photoId, text) => {
        await gql(
            `
            mutation($photoId: ID!, $text: String!) {
                createComment(photoId: $photoId, text: $text) {
                    comment {
                        id
                        text
                    }
                }
            }
        `,
            {photoId, text}
        );

        await loadPhotos();
    };

    const searchPhotos = async () => {
        if (!search.trim()) {
            await loadPhotos();
            return;
        }

        const result = await gql(
            `
                query($query: String!) {
                    searchPhotos(query: $query) {
                        id
                        image
                        caption
                        tags
                        likesCount
                    }
                }
            `,
            {query: search}
        );

        setPhotos(result.data?.searchPhotos || []);
    };

    const createPhoto = async (caption, tags, imageBase64) => {
        await gql(
            `
                mutation($caption: String, $tags: [String], $imageBase64: String) {
                    createPhoto(
                        caption: $caption,
                        tags: $tags,
                        imageBase64: $imageBase64
                    ) {
                        photo {
                            id
                            image
                            caption
                            tags
                            likesCount
                        }
                    }
                }
            `,
            {caption, tags, imageBase64}
        );

        setToast("Фото опубліковано");
        await loadPhotos();
    };

    const likePhoto = async (photoId) => {
        await gql(
            `
                mutation($photoId: ID!) {
                    toggleLike(photoId: $photoId) {
                        photo {
                            id
                            likesCount
                        }
                    }
                }
            `,
            {photoId}
        );

        await loadPhotos();
    };

    useEffect(() => {
        loadPhotos();
    }, []);

    return (
        <main className="container py-4">
            <ToastMessage message={toast} onClose={() => setToast("")}/>
            <UploadModal onCreate={createPhoto}/>

            <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
                <div>
                    <h1 className="fw-bold mb-1">InstaPhoto</h1>
                    <p className="text-muted mb-0">
                        Ділись фотографіями, став лайки та знаходь цікаві публікації.
                    </p>
                </div>

                <button
                    className="btn btn-primary px-4"
                    data-bs-toggle="modal"
                    data-bs-target="#uploadModal"
                >
                    + Додати фото
                </button>
            </div>

            <div className="card border-0 shadow-sm mb-4">
                <div className="card-body">
                    <div className="input-group">
                        <input
                            className="form-control"
                            value={search}
                            onChange={(event) => setSearch(event.target.value)}
                            placeholder="Пошук за тегами або описом"
                        />

                        <button className="btn btn-dark" onClick={searchPhotos}>
                            Шукати
                        </button>
                    </div>
                </div>
            </div>

            {photos.length === 0 ? (
                <div className="text-center py-5">
                    <div className="display-4 mb-3">📷</div>
                    <h5 className="fw-bold">Поки що немає фото</h5>
                    <p className="text-muted mb-4">
                        Додай першу публікацію на платформу.
                    </p>

                    <button
                        className="btn btn-primary"
                        data-bs-toggle="modal"
                        data-bs-target="#uploadModal"
                    >
                        Додати фото
                    </button>
                </div>
            ) : (
                <div className="row g-4">
                    {photos.map((photo) => (
                        <PhotoCard
                            photo={photo}
                            onLike={likePhoto}
                            onComment={createComment}
                        />
                    ))}
                </div>
            )}
        </main>
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(
    <App/>
);