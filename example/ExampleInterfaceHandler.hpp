#pragma once

#include <nlohmann/json.hpp>
#include "ExampleInterface.hpp"
#include <iostream>

using json = nlohmann::json;

void to_json(
        json& j,
        const Dummy& Dummy)
{
    j = json{ {"a", Dummy.a}, {"b", Dummy.b}};
}

void from_json(
        const json& j,
        Dummy& Dummy)
{
    j.at("a").get_to(Dummy.a);
    j.at("b").get_to(Dummy.b);
}

class ExampleInterfaceDummyImpl: public ExampleInterface
{
    public:
    json metodo_uno(int a) const noexcept
    {
        json ret {};
        ret["ret"] = a;
        return ret;
    }

    json metodo_dos(float a, std::string b) const noexcept
    {
        json ret {};
        ret["ret"] = std::to_string(a) + " " + b;
        return ret;
    }

    json metodo_tres(const Dummy & input) const noexcept
    {
        json ret = input;
        return ret;
    }

    Dummy metodo_cuatro(const Dummy & input) const noexcept
    {
        return input;
    }

    int metodo_cinco(int a) const noexcept
    {
        return a;
    }
};


struct ExampleInterface_Handler
{
    static ExampleInterface& get_instance() noexcept

    {
        static ExampleInterfaceDummyImpl imp{};
        return imp;
    }
};