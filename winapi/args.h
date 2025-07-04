// Command line argument parsing utility
// 
// Copyright (C) 2023 - 2024 Bryan Morabito

#pragma once

#include <array>
#include <string>
#include <vector>
#include <memory>
#include <iomanip>
#include <sstream>
#include <iostream>
#include <concepts>
#include <initializer_list>
#include <algorithm>
#include <functional>

template<typename... T>
consteval auto make_array(T&&... values) ->
std::array<
    typename std::decay<
    typename std::common_type<T...>::type
    >::type,
    sizeof...(T)
> {
    return std::array<
        typename std::decay<
        typename std::common_type<T...>::type
        >::type,
        sizeof... (T)
    > { std::forward<T>(values)... };
}

namespace args {
    template<typename CharT>
    class basic_args {
    public:
        using const_pointer          = const CharT*;
        using string                 = std::basic_string<CharT>;
        using vector                 = std::vector<string>;

        using iterator               = typename vector::              iterator;
        using const_iterator         = typename vector::        const_iterator;
        using reverse_iterator       = typename vector::      reverse_iterator;
        using const_reverse_iterator = typename vector::const_reverse_iterator;

    protected:
        vector args;

    public:
        basic_args(size_t        argc,
                   const_pointer argv[]) {
            for (size_t i = 1; i < argc; i++) args.push_back(argv[i]);
        }

        [[nodiscard]] constexpr               iterator   begin()       noexcept { return args.  begin(); }
        [[nodiscard]] constexpr         const_iterator   begin() const noexcept { return args. cbegin(); }
        [[nodiscard]] constexpr               iterator     end()       noexcept { return args.    end(); }
        [[nodiscard]] constexpr         const_iterator     end() const noexcept { return args.   cend(); }
        [[nodiscard]] constexpr       reverse_iterator  rbegin()       noexcept { return args. rbegin(); }
        [[nodiscard]] constexpr const_reverse_iterator  rbegin() const noexcept { return args.crbegin(); }
        [[nodiscard]] constexpr       reverse_iterator    rend()       noexcept { return args.   rend(); }
        [[nodiscard]] constexpr const_reverse_iterator    rend() const noexcept { return args.  crend(); }
        [[nodiscard]] constexpr         const_iterator  cbegin() const noexcept { return args. cbegin(); }
        [[nodiscard]] constexpr         const_iterator    cend() const noexcept { return args.   cend(); }
        [[nodiscard]] constexpr const_reverse_iterator crbegin() const noexcept { return args.crbegin(); }
        [[nodiscard]] constexpr const_reverse_iterator   crend() const noexcept { return args.  crend(); }
    };

    using  args = basic_args< char>;
    using wargs = basic_args<wchar_t>;

    template<typename CharT>
    class basic_option_impl {
    public:
        using const_pointer    = const CharT*;
        using string           = std::basic_string<CharT>;
        using ostream          = std::basic_ostream<CharT>;
        using initializer_list = std::initializer_list<string>;

        using args_type        = basic_args<CharT>;

        using vector           = args_type::vector;

        template<size_t N>
        using array = std::array<const_pointer, N>;

        static constexpr size_t alias_string_length = 32;

    public:
        vector aliases;
        string description;
        string suffix;

        typename args_type::iterator find_in_args(args_type& args) {
            return std::find_first_of(args.begin(), args.end(), aliases.begin(), aliases.end());
        }

        bool contained_in_args(args_type args) {
            return find_in_args(args) != args.end();
        }

    public:
        basic_option_impl(initializer_list aliases,
                          string           description,
                          string           suffix = "") :
            aliases(aliases),
            description(description),
            suffix(suffix) { }

        template<size_t alias_count>
        basic_option_impl(array<alias_count> aliases,
                          string             description,
                          string             suffix = { }) :
            aliases(aliases.begin(), aliases.end()),
            description(description),
            suffix(suffix) { }

        virtual bool operator()(args_type) = 0;

        friend ostream& operator<<(ostream& lhs, basic_option_impl& rhs) {
            if (rhs.aliases.size() == 0) return lhs;

            string aliases_string = rhs.aliases[0];

            for (size_t i = 1; i < rhs.aliases.size(); i++) {
                string str = aliases_string + L", " + rhs.aliases[i];

                if (str.size() > alias_string_length) break;
                aliases_string = str;
            }

            if (rhs.suffix.size() > 0) aliases_string += L" <" + rhs.suffix + L">";

            return lhs << "    " << aliases_string << std::setw(alias_string_length - aliases_string.size() + 1) << std::setfill(L' ') << ' ' << rhs.description << std::endl;
        }
    };

    template<typename CharT, typename FunctionT>
    class basic_option : public basic_option_impl<CharT> {
    public:
        using option_impl      = basic_option_impl<CharT>;
        using const_pointer    = typename option_impl::const_pointer;
        using initializer_list = typename option_impl::initializer_list;
        using string           = typename option_impl::string;
        using args_type        = typename option_impl::args_type;

        template<size_t N>
        using array = std::array<const_pointer, N>;

        using      function    = std::function<FunctionT>;
        using move_function    = std::function<FunctionT>&&;

    private:
        function option_handler;

    public:
        basic_option(initializer_list aliases,
                     string           description,
                     move_function    option_handler) :
            option_impl(aliases, description),
            option_handler(option_handler) { }

        template<size_t alias_count>
        basic_option(array<alias_count> aliases,
                     string             description,
                     move_function      option_handler) :
            option_impl(aliases, description),
            option_handler(option_handler) { }

        bool operator()(args_type args) {
            if (option_impl::contained_in_args(args))
                option_handler();

            return true;
        }
    };

    template<typename FunctionT>
    using  option = basic_option< char,   FunctionT>;

    template<typename FunctionT>
    using woption = basic_option<wchar_t, FunctionT>;

    template<typename CharT, typename ValueT>
    class basic_argument : public basic_option_impl<CharT> {
    private:
        using option_impl      = basic_option_impl<CharT>;
        using const_pointer    = typename option_impl::const_pointer;
        using initializer_list = typename option_impl::initializer_list;
        using string           = typename option_impl::string;
        using args_type        = typename option_impl::args_type;

        template<size_t N>
        using array = std::array<const_pointer, N>;

        using reference_type   = ValueT&;
        using pointer          = ValueT*;
        using isstream         = std::basic_istringstream<CharT>;
        using osstream         = std::basic_ostringstream<CharT>;

        pointer ptr;

    public:
        basic_argument(initializer_list aliases,
                       string           description,
                       string           parameter_name,
                       reference_type   reference,
                       bool             print_default = true) :
            option_impl(aliases, description + (print_default ? (L" (default: " + toString(reference) + L")") : L""), parameter_name),
            ptr(&reference) { }

        basic_argument(initializer_list aliases,
                       string           description,
                       string           parameter_name,
                       pointer          ptr,
                       bool             print_default = true) :
            option_impl(aliases, description + (print_default ? (L" (default: " + toString(*ptr) + L")") : L""), parameter_name),
            ptr(ptr) { }

        template<size_t alias_count>
        basic_argument(array<alias_count> aliases,
                       string             description,
                       string             parameter_name,
                       reference_type     reference,
                       bool             print_default = true) :
            option_impl(aliases, description + (print_default ? (L" (default: " + toString(reference) + L")") : L""), parameter_name),
            ptr(&reference) { }

        template<size_t alias_count>
        basic_argument(array<alias_count> aliases,
                       string             description,
                       string             parameter_name,
                       pointer            ptr,
                       bool             print_default = true) :
            option_impl(aliases, description + (print_default ? (L" (default: " + toString(*ptr) + L")") : L""), parameter_name),
            ptr(ptr) { }

        bool get_arg_others(args_type args) requires (!std::same_as<ValueT, string>) {
            auto iterator = option_impl::find_in_args(args);

            if (iterator != args.end()) {
                if (++iterator == args.end())
                    return false;

                isstream stream { *iterator };
                stream >> *ptr;
            }

            return true;
        }

        bool get_arg_string(args_type args) requires (std::same_as<ValueT, string>) {
            auto iterator = option_impl::find_in_args(args);

            if (iterator != args.end()) {
                if (++iterator == args.end())
                    return false;

                *ptr = *iterator;
            }

            return true;
        }
        
        bool operator()(args_type args) {
            if constexpr (std::same_as<ValueT, string>) return get_arg_string(args);
            else                                        return get_arg_others(args);
        }

        string toString(ValueT value) {
            osstream stream { };

            stream << value;

            return stream.str();
        }
    };

    template<typename ValueT>
    using  argument = basic_argument< char,   ValueT>;

    template<typename ValueT>
    using wargument = basic_argument<wchar_t, ValueT>;

    template<typename CharT>
    class basic_arg_parser {
    public:
        using args_type      = basic_args<CharT>;
        using option_impl    = std::shared_ptr<basic_option_impl<CharT>>;
        using options_vector = std::vector<std::shared_ptr<basic_option_impl<CharT>>>;
        using string         = std::basic_string<CharT>;

    private:
        options_vector options;
        args_type      args;
        string         description;

    public:
        basic_arg_parser(args_type args,
                         string    description) :
            options(),
            args(args),
            description(description) { }

        template<typename FunctionT>
        basic_arg_parser& operator<<(basic_option<CharT, FunctionT>&& option) {
            options.push_back((option_impl)std::make_shared<basic_option<CharT, FunctionT>>(option));
            return *this;
        }

        template<typename ValueT>
        basic_arg_parser& operator<<(basic_argument<CharT, ValueT>&& argument) {
            options.push_back((option_impl)std::make_shared<basic_argument<CharT, ValueT>>(argument));
            return *this;
        }

        static void help(const basic_arg_parser& parser) {
            std::wcout << parser.description << std::endl
                      << std::endl;

            for (auto& option : parser.options)
                std::wcout << *option;
        }

        void operator()() {
            for (auto& option : options) {
                if (!option->operator()(args)) {
                    help(*this);
                    std::abort();
                }
            }
        }

        std::string& getDescription() { return description; }
    };

    using  parser = basic_arg_parser< char  >;
    using wparser = basic_arg_parser<wchar_t>;
}
