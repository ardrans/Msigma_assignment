import React, { useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import PhoneInput, { isValidPhoneNumber } from 'react-phone-number-input';
import { Form, Button, Alert, Spinner, Card } from 'react-bootstrap';
import 'react-phone-number-input/style.css';
import './FormPage.css';
import { createRecord } from '../services/api';

// Validation schema
const schema = yup.object().shape({
  name: yup
    .string()
    .required('Name is required')
    .min(2, 'Name must be at least 2 characters')
    .max(255, 'Name cannot exceed 255 characters'),
  email: yup
    .string()
    .required('Email is required')
    .email('Invalid email format'),
  phone_number: yup
    .string()
    .required('Phone number is required')
    .test('is-valid-phone', 'Invalid phone number', (value) => {
      return value ? isValidPhoneNumber(value) : false;
    }),
  link: yup
    .string()
    .nullable()
    .transform((value) => (value === '' ? null : value))
    .url('Invalid URL format (must start with http:// or https://)'),
  dob: yup
    .string()
    .nullable()
    .transform((value) => (value === '' ? null : value))
    .test('is-valid-date', 'Invalid date', (value) => {
      if (!value) return true;
      const date = new Date(value);
      return date instanceof Date && !isNaN(date) && date <= new Date();
    }),
});

const FormPage = ({ onSuccess }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      name: '',
      email: '',
      phone_number: '',
      link: '',
      dob: '',
    },
  });

  const onSubmit = async (data) => {
    setIsSubmitting(true);
    setSubmitError(null);
    setSubmitSuccess(false);

    try {
      await createRecord(data);
      setSubmitSuccess(true);
      reset();
      if (onSuccess) onSuccess();
    } catch (error) {
      setSubmitError(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="form-card">
      <Card.Body>
        <Card.Title className="text-center mb-4">
          <h2>New Record Submission</h2>
        </Card.Title>

        {submitSuccess && (
          <Alert variant="success" dismissible onClose={() => setSubmitSuccess(false)}>
            Record submitted successfully!
          </Alert>
        )}

        {submitError && (
          <Alert variant="danger" dismissible onClose={() => setSubmitError(null)}>
            {submitError}
          </Alert>
        )}

        <Form onSubmit={handleSubmit(onSubmit)} noValidate>
          {/* Name Field */}
          <Form.Group className="mb-3" controlId="name">
            <Form.Label>Name *</Form.Label>
            <Form.Control
              type="text"
              placeholder="Ardra"
              {...register('name')}
              isInvalid={!!errors.name}
            />
            <Form.Control.Feedback type="invalid">
              {errors.name?.message}
            </Form.Control.Feedback>
          </Form.Group>

          {/* Email Field */}
          <Form.Group className="mb-3" controlId="email">
            <Form.Label>Email *</Form.Label>
            <Form.Control
              type="email"
              placeholder="ardra@example.com"
              {...register('email')}
              isInvalid={!!errors.email}
            />
            <Form.Control.Feedback type="invalid">
              {errors.email?.message}
            </Form.Control.Feedback>
          </Form.Group>

          {/* Phone Number Field */}
          <Form.Group className="mb-3" controlId="phone_number">
            <Form.Label>Phone Number *</Form.Label>
            <Controller
              name="phone_number"
              control={control}
              render={({ field }) => (
                <PhoneInput
                  {...field}
                  international
                  defaultCountry="IN"
                  placeholder="Enter phone number"
                  className={`form-control phone-input ${errors.phone_number ? 'is-invalid' : ''}`}
                />
              )}
            />
            {errors.phone_number && (
              <div className="invalid-feedback d-block">
                {errors.phone_number.message}
              </div>
            )}
          </Form.Group>

          {/* Link Field (Optional) */}
          <Form.Group className="mb-3" controlId="link">
            <Form.Label>Portfolio / GitHub / LinkedIn URL</Form.Label>
            <Form.Control
              type="url"
              placeholder="https://github.com/username"
              {...register('link')}
              isInvalid={!!errors.link}
            />
            <Form.Control.Feedback type="invalid">
              {errors.link?.message}
            </Form.Control.Feedback>
          </Form.Group>

          {/* DOB Field (Optional) */}
          <Form.Group className="mb-4" controlId="dob">
            <Form.Label>Date of Birth</Form.Label>
            <Form.Control
              type="date"
              {...register('dob')}
              isInvalid={!!errors.dob}
              max={new Date().toISOString().split('T')[0]}
            />
            <Form.Control.Feedback type="invalid">
              {errors.dob?.message}
            </Form.Control.Feedback>
          </Form.Group>

          {/* Submit Button */}
          <div className="d-grid">
            <Button
              variant="primary"
              type="submit"
              size="lg"
              disabled={isSubmitting}
              className="submit-btn"
            >
              {isSubmitting ? (
                <>
                  <Spinner
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                    className="me-2"
                  />
                  Submitting...
                </>
              ) : (
                'Submit for Processing'
              )}
            </Button>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default FormPage;
