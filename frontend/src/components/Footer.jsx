export default function Footer() {
  return (
    <footer className="mt-12 border-t border-slate-800 pt-6 text-xs text-slate-500">
      <div className="flex flex-col items-center gap-3 text-center sm:flex-row sm:justify-between sm:text-left">
        {/* Profile Image */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 overflow-hidden rounded-full border border-slate-700/80 bg-slate-900 sm:h-9 sm:w-9">
            <img
              src="/token.png"
              alt="Crispin portrait"
              className="h-full w-full object-cover"
            />
          </div>
        </div>

        {/* Copyright */}
        <p className="text-slate-600">
          © 2024 Crispin Niyomwungeri. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
