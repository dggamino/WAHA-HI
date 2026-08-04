"""Custom exceptions."""
class WahaHiRuntimeError(Exception): pass
class ConfigurationError(WahaHiRuntimeError): pass
class ValidationError(WahaHiRuntimeError): pass
class EnvironmentError(WahaHiRuntimeError): pass
class PathResolutionError(WahaHiRuntimeError): pass
class EngineError(WahaHiRuntimeError): pass
