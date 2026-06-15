import Select, { StylesConfig } from 'react-select';

export type SelectWithSearchItem = {
  id: string;
  name: string;
};

type Option = {
  value: string;
  label: string;
};

type SelectWithSearch = {
  items: SelectWithSearchItem[];
  value: string;
  onChange: (id: string) => void;
  placeholder?: string;
  label?: string;
  disabled?: boolean;
};

const styles: StylesConfig<Option, false> = {
  control: (base, state) => ({
    ...base,
    minHeight: 42,
    borderRadius: 12,
    borderColor: state.isFocused ? '#3b82f6' : '#cbd5e1',
    boxShadow: state.isFocused ? '0 0 0 1px #3b82f6' : 'none',
    '&:hover': {
      borderColor: state.isFocused ? '#3b82f6' : '#94a3b8',
    },
  }),
  option: (base, state) => ({
    ...base,
    backgroundColor: state.isSelected ? '#dbeafe' : state.isFocused ? '#f1f5f9' : '#ffffff',
    color: '#0f172a',
    cursor: 'pointer',
  }),
};

export function SelectWithSearch({
  items,
  value,
  onChange,
  placeholder = 'Buscar...',
  label,
  disabled = false,
}: SelectWithSearch) {
  const options: Option[] = items.map((item) => ({
    value: item.id,
    label: item.name,
  }));

  const selectedOption = options.find((option) => option.value === value) ?? null;

  return (
    <div className="field-group">
      {label && <label>{label}</label>}
      <Select<Option, false>
        options={options}
        value={selectedOption}
        onChange={(option) => onChange(option?.value ?? '')}
        placeholder={placeholder}
        isSearchable
        isClearable
        isDisabled={disabled}
        noOptionsMessage={() => 'Nenhum resultado'}
        menuPortalTarget={typeof window !== 'undefined' ? document.body : null}
        styles={styles}
        classNamePrefix="select-search"
        classNames={{
          input: () => '[&>input]:!outline-none [&>input]:!ring-0',
        }}
        aria-label={label ?? placeholder}
      />
    </div>
  );
}
