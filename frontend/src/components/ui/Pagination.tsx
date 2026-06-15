'use client';

interface Props {
  count: number;
  currentPage: number;
  totalPages: number;
  pageSize?: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ count, currentPage, totalPages, pageSize = 10, onPageChange }: Props) {
  if (totalPages <= 1) return null;

  const startItem = (currentPage - 1) * pageSize + 1;
  const endItem = Math.min(currentPage * pageSize, count);

  const pages = Array.from({ length: totalPages }, (_, index) => index + 1).filter((page) => {
    return (
      page === 1 ||
      page === totalPages ||
      Math.abs(page - currentPage) <= 1
    );
  });

  const compactPages = pages.reduce<number[]>((acc, page) => {
    if (acc.length > 0 && page - acc[acc.length - 1] > 1) {
      acc.push(-1);
    }
    acc.push(page);
    return acc;
  }, []);

  return (
    <div className="flex flex-col gap-3 border-t border-slate-100 dark:border-slate-800 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="text-sm text-slate-400 dark:text-slate-500">
        Mostrando {startItem}-{endItem} de {count} registros
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <button
          className="btn btn-secondary btn-sm"
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          Anterior
        </button>

        {compactPages.map((page, index) => (
          page === -1 ? (
            <span key={`ellipsis-${index}`} className="px-1 text-slate-400 dark:text-slate-500">...</span>
          ) : (
            <button
              key={page}
              className={`btn btn-sm ${page === currentPage ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => onPageChange(page)}
            >
              {page}
            </button>
          )
        ))}

        <button
          className="btn btn-secondary btn-sm"
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          Próxima
        </button>
      </div>
    </div>
  );
}
