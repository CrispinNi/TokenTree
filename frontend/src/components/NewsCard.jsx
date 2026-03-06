export default function NewsCard({ item }) {
  const publishedDate = item.published_at
    ? new Date(item.published_at * 1000).toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      })
    : "Unknown date";

  return (
    <a
      href={item.url}
      target="_blank"
      rel="noreferrer"
      className="group bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 flex flex-col h-full"
    >
      {/* Image Container */}
      <div className="relative h-48 bg-slate-700 overflow-hidden">
        {item.image ? (
          <img
            src={item.image}
            alt={item.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600">
            <span className="text-white text-3xl">📰</span>
          </div>
        )}
      </div>

      {/* Content Container */}
      <div className="p-4 flex flex-col flex-grow">
        {/* Title */}
        <h3 className="text-sm font-semibold text-white group-hover:text-blue-300 transition-colors duration-200 line-clamp-2 mb-2">
          {item.title}
        </h3>

        {/* Source and Date */}
        <div className="mt-auto pt-3 border-t border-slate-700">
          <div className="flex justify-between items-center text-xs text-slate-400">
            <span className="font-medium text-blue-400">
              {item.source || "Crypto News"}
            </span>
            <span>{publishedDate}</span>
          </div>
        </div>
      </div>
    </a>
  );
}
